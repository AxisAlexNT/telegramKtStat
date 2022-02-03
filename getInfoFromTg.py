import json
from transliterate import translit, get_available_language_codes
import Levenshtein
import matplotlib.pyplot as plt

from telethon import functions
from telethon.sync import TelegramClient

api_id = 18442708
api_hash = '72cf2c0dfa15679f1a96e3fab43728a5'
required_chats = [-1001566274537, -1001595810251, -1001487603470] #y2021 dm prog
def getNames():
    client = TelegramClient('count', api_id, api_hash)
    client.start()
    data = {}
    with open("data.json", 'r') as data_file:
        data = json.load(data_file)
    new_data = {}
    group_data = {}
    with open("groups_data.json", 'r') as data_file:
        group_data = json.load(data_file)
    y2021 = set()
    for dialog in client.iter_dialogs():
        part = set()
        if dialog.id not in required_chats:
            continue
        for student in client.iter_participants(dialog.name):
            part.add(student.id)
        if len(y2021) == 0:
            y2021 = part
        else:
            y2021 = y2021 & part
    count_groups = {"others":0}
    bad_students = {}
    with open("bad_names.json", 'r') as data_file:
        bad_students = json.load(data_file) # type: dict
    for student in client.iter_participants('КТ y2021'):
        # if student.id not in y2021:
        #     continue
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
                    "second_name" : student_name.split()[0],
                    "full_name" : student_name,
                    "username" : student.username,
                    "group" : group,
                    "messages" : data[str(student.id)].copy()
                }
                break
    with open("data.json", "w") as data_file:
        json.dump(new_data, data_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    getNames()