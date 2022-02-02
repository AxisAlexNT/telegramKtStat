import json

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
    for student in client.iter_participants('КТ y2021'):
        if student.id not in y2021:
            continue
        if not student.first_name or not student.last_name:
            continue
        for student_name in group_data.keys():
            if (student.first_name in student_name and student.last_name in student_name):
                print(student.first_name, student.last_name, group_data[student_name])
                break
        else:
            if student.id not in data.keys():
                continue
            print(student.username, student.first_name, student.last_name, data[str(student.id)][str(-1001566274537)])
            if (data[student.id][-1001566274537] > 100):
                pass



if __name__ == '__main__':
    getNames()