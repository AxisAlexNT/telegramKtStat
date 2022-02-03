import datetime
import json

from telethon import TelegramClient, sync

api_id = 18442708
api_hash = '72cf2c0dfa15679f1a96e3fab43728a5'
def getChat():
    client = TelegramClient('count', api_id, api_hash)
    client.start()
    for dialog in client.iter_dialogs():
        print(dialog.title, dialog.id)



if __name__ == '__main__':
    getChat()