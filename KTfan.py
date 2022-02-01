class KTfan(object):
    def __init__(self, id):
        self.id = id
        self.messages = {}

    # def __init__(self, id, tag, tg_firstname, tg_secondname):
    #     self.id = id
    #     self.tag = tag
    #     self.tg_firstname = tg_firstname
    #     self.tg_secondname = tg_secondname
    #     self.messages = {}
    #     self.messages.setdefault(0)

    def add_message(self, chat_id):
        if chat_id in self.messages.keys():
            self.messages[chat_id] += 1
        else:
            self.messages[chat_id] = 1

    def __eq__(self, other):
        return self.id == other.id
    def __str__(self):
        return f'KTfan(id={self.id},\nmessages={self.messages}'