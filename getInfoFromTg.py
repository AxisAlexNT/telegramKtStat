import json

from telethon import TelegramClient

def getNames():
    client = TelegramClient('count', api_id, api_hash)
    client.start()
    data = {}
    with open("data.json", 'r') as data_file:
        data = json.load(data_file)
    new_data = {}
    for id in data.keys():
        print(client.get_peer_id(id))


if __name__ == '__main__':
    getNames()