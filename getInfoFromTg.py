import datetime
import json
import os
import Levenshtein
from telethon import TelegramClient
from transliterate import translit

api_id = 18442708
api_hash = '72cf2c0dfa15679f1a96e3fab43728a5'


def getMessages():
    kt_fans = {}
    for file in os.listdir("chats"):
        with open("chats/" + file, 'r') as data_file:
            dialog = json.load(data_file)  # type: dict
        for message in dialog["messages"]:  # type: dict
            if message["type"] != "message":
                continue
            if isinstance(message["text"], dict):
                message["text"] = message["text"]["text"]
            if message["from_id"] not in kt_fans.keys():
                kt_fans[message["from_id"]] = {}

            if dialog["id"] in kt_fans[message["from_id"]].keys():
                kt_fans[message["from_id"]][dialog["id"]]["count"] += 1
                kt_fans[message["from_id"]][dialog["id"]]["length"] += len(message["text"])
                kt_fans[message["from_id"]][dialog["id"]]["max_length"] = max(len(message["text"]),
                                                                              kt_fans[message["from_id"]][dialog["id"]]["max_length"])
            else:
                kt_fans[message["from_id"]][dialog["id"]] = {"count": 1,
                                                             "length": len(message["text"]),
                                                             "max_length": len(message["text"])}

    with open("raw_data.json", 'w') as data_file:
        json.dump(kt_fans, data_file)


def getNames():
    client = TelegramClient('count', api_id, api_hash)
    client.start()
    with open("raw_data.json", 'r') as data_file:
        data = json.load(data_file)
    new_data = {}
    with open("groups_data.json", 'r') as data_file:
        group_data = json.load(data_file)
    with open("bad_names.json", 'r') as data_file:
        bad_students = json.load(data_file)  # type: dict
    dialogs = client.get_dialogs()
    for student_id in data.keys():
        if not student_id.startswith("user"):
            continue
        try:
            student = client.get_entity(int(student_id[4:]))
        except ValueError:
            print("Can't find entity: " + student_id)
            continue
        if not student.first_name or not student.last_name:
            new_data[str(student.id)] = {
                "first_name": "",
                "last_name": "",
                "full_name": "",
                "username": student.username,
                "group": "others",
                "messages": data.get(student_id, {}).copy()
            }
            continue
        student.first_name = translit(student.first_name.split()[0], 'ru').capitalize()
        student.last_name = translit(student.last_name.split()[0], 'ru').capitalize()
        if student.username in bad_students.keys():
            student.first_name = bad_students[student.username]["first_name"]
            student.last_name = bad_students[student.username]["last_name"]
        for student_name in group_data.keys():
            if (Levenshtein.distance(student.first_name, student_name.split()[1]) <= 2 and
                    Levenshtein.distance(student.last_name, student_name.split()[0]) <= 2):
                group = group_data[student_name]
                new_data[str(student.id)] = {
                    "first_name": student_name.split()[1],
                    "last_name": student_name.split()[0],
                    "full_name": student_name,
                    "username": student.username,
                    "group": group,
                    "messages": data.get(student_id, {}).copy()
                }
                break
        else:
            new_data[str(student.id)] = {
                "first_name": student.first_name,
                "last_name": student.last_name,
                "full_name": student.last_name + " " + student.first_name,
                "username": student.username,
                "group": "others",
                "messages": data.get(str(student.id), {}).copy()
            }
    with open("data.json", "w") as data_file:
        json.dump(new_data, data_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    getMessages()
    getNames()
