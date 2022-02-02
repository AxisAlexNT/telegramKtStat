import datetime
import json

from telethon import TelegramClient, sync

from KTfan import KTfan

api_id = 18442708
api_hash = '72cf2c0dfa15679f1a96e3fab43728a5'
flud_dialogs = [-1001083494173, -1001358584131, -1001186169699, -1001566274537]
study_dialogs = [-1001509453723, -1001595810251, -1001487603470, -1001419469399, -1001551100526, -1001592102255, -1001695358795]
dialogs = flud_dialogs + study_dialogs
def getMessages():
    client = TelegramClient('count', api_id, api_hash)
    client.start()
    kt_fans = {}
    for dialog in client.iter_dialogs():
        if dialog.id in flud_dialogs or dialog.id in study_dialogs:
            print(dialog.title, dialog.id)
            # continue
            for message in client.iter_messages(dialog.title):
                if not hasattr(message.from_id, 'user_id'):
                    continue
                if message.date.date() < datetime.date(2021, 8, 12):
                    break
                if message.from_id.user_id not in kt_fans.keys():
                    kt_fans[message.from_id.user_id] = {}
                if dialog.id in kt_fans[message.from_id.user_id].keys():
                    kt_fans[message.from_id.user_id][dialog.id] += 1
                else:
                    kt_fans[message.from_id.user_id][dialog.id] = 1
                with open("data.json", 'w') as data_file:
                    json.dump(kt_fans, data_file)


if __name__ == '__main__':
    getMessages()