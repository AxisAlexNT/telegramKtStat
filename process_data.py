import json
from collections import Counter

import numpy as np
from matplotlib import pyplot as plt

flud_dialogs = [-1001083494173, -1001358584131, -1001186169699, -1001566274537]
study_dialogs = [-1001509453723, -1001595810251, -1001487603470, -1001419469399, -1001551100526, -1001592102255, -1001695358795]
def get3839group_stat(arg : str):
    data = {}
    with open("data.json", 'r') as data_file:
        data = json.load(data_file) # type: dict
    chat_id = "-1001186169699"
    count_group = Counter()
    for student in data.values(): # type: dict
        if student["group"] in ["M3138", "M3139"]:
            count_group[student["group"]] += student["messages"].get(chat_id, {arg:0})[arg]
    print(count_group)
    labels = sorted(list(count_group.keys()))
    values = [count_group[labels[i]] for i in range(len(labels))]
    fig, ax = plt.subplots()
    ax.bar_label(ax.bar(labels, values, 0.35))
    ax.set_ylabel('Messages')
    ax.set_title(arg + ' messages in M3138-39')

    plt.show()
def get3839personal_stat(arg : str):
    data = {}
    with open("data.json", 'r') as data_file:
        data = json.load(data_file)  # type: dict
    chat_id = "-1001186169699"
    count = Counter()
    for student in data.values():  # type: dict
        if student["group"] in ["M3138", "M3139"]:
            count[student["full_name"]] = student["messages"].get(chat_id, {arg:0})[arg]


    print(count)
    labels = sorted(list(count.keys()), key=(lambda x : count[x]))
    values = [count[labels[i]] for i in range(len(labels))]
    position = np.arange(len(labels))

    fig, ax = plt.subplots()

    ax.bar_label(ax.barh(position, values))

    ax.set_yticks(position)

    labels = ax.set_yticklabels(labels)

    fig.set_figwidth(22)
    fig.set_figheight(15)
    plt.show()
def get_y2021_group_stat(arg : str):
    data = {}
    with open("data.json", 'r') as data_file:
        data = json.load(data_file)  # type: dict
    chat_id = "-1001566274537"
    count_group = Counter()
    for student in data.values():  # type: dict
        count_group[student["group"]] += student["messages"].get(chat_id, {arg: 0})[arg]
    print(count_group)
    labels = sorted(list(count_group.keys()))
    values = [count_group[labels[i]] for i in range(len(labels))]
    fig, ax = plt.subplots()
    ax.bar_label(ax.bar(labels, values, 0.35))
    ax.set_ylabel('Messages')
    ax.set_title(arg + ' messages in y2021')

    plt.show()
if __name__ == "__main__":
    get_y2021_group_stat("length")
    # get3839group_stat("length")
    # get3839personal_stat("max_length")