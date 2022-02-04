import datetime
import json

import Levenshtein
from telethon import TelegramClient, sync
from transliterate import translit

api_id = 18442708
api_hash = '72cf2c0dfa15679f1a96e3fab43728a5'
dialogs = [-1001083494173, -1001358584131, -1001186169699, -100156627453,
           -1001509453723, -1001595810251, -1001487603470, -1001419469399,
           -1001551100526, -1001592102255, -1001695358795, -1001566274537]
def getMessages():
    client = TelegramClient('count', api_id, api_hash)
    client.start()
    kt_fans = {}
    for dialog in client.iter_dialogs():
        if dialog.id not in dialogs:
            continue
        print(dialog.title, dialog.id)
        for message in client.iter_messages(dialog.title):
            if not hasattr(message.from_id, 'user_id'):
                continue
            if message.date.date() < datetime.date(2021, 8, 12):
                break
            # print(message.stringify())
            # break
            message.message = message.message if message.message else ''
            if message.from_id.user_id not in kt_fans.keys():
                kt_fans[message.from_id.user_id] = {}
            if dialog.id in kt_fans[message.from_id.user_id].keys():
                kt_fans[message.from_id.user_id][dialog.id]["count"] += 1
                kt_fans[message.from_id.user_id][dialog.id]["length"] += len(message.message)
                kt_fans[message.from_id.user_id][dialog.id]["max_length"] = max(len(message.message),
                                                                                kt_fans[message.from_id.user_id][dialog.id]["max_length"])
            else:
                kt_fans[message.from_id.user_id][dialog.id] = {"count" : 1,
                                                               "length" : len(message.message),
                                                               "max_length":len(message.message)}
        with open("raw_data.json", 'w') as data_file:
            json.dump(kt_fans, data_file)

def getNames():
    client = TelegramClient('count', api_id, api_hash)
    client.start()
    data = {}
    with open("raw_data.json", 'r') as data_file:
        data = json.load(data_file)
    new_data = {}
    group_data = {}
    with open("groups_data.json", 'r') as data_file:
        group_data = json.load(data_file)
    count_groups = {"others" : 0}
    bad_students = {}
    with open("bad_names.json", 'r') as data_file:
        bad_students = json.load(data_file) # type: dict
    for student in client.iter_participants('КТ y2021'):
        if not student.first_name or not student.last_name:
            continue
        if str(student.id) not in data.keys():
            data[str(student.id)] = {}
        student.first_name = translit(student.first_name.split()[0], 'ru').capitalize()
        student.last_name = translit(student.last_name.split()[0], 'ru').capitalize()
        if (student.username in bad_students.keys()):
            student.first_name = bad_students[student.username]["first_name"]
            student.last_name = bad_students[student.username]["last_name"]
        for student_name in group_data.keys():
            if (Levenshtein.distance(student.first_name, student_name.split()[1]) <= 2 and
                    Levenshtein.distance(student.last_name, student_name.split()[0]) <= 2):
                group = group_data[student_name]
                new_data[str(student.id)] = {
                    "first_name" : student_name.split()[1],
                    "last_name" : student_name.split()[0],
                    "full_name" : student_name,
                    "username" : student.username,
                    "group" : group,
                    "messages" : data[str(student.id)].copy()
                }
                break
        else:
            new_data[str(student.id)] = {
                "first_name": student.first_name,
                "last_name": student.last_name,
                "full_name": student.last_name + " " + student.first_name,
                "username": student.username,
                "group": "others",
                "messages": data[str(student.id)].copy()
            }
    with open("data.json", "w") as data_file:
        json.dump(new_data, data_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    #getMessages()
    getNames()