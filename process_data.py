import json
from collections import Counter

import numpy as np
from matplotlib import pyplot as plt

flud_3839_dialogs = ["1001083494173", "1001358584131", "1001186169699", "1001566274537"]
study_3839_dialogs = ["1001509453723", "1001595810251", "1001487603470", "1001419469399",
                 "1001551100526", "1001592102255", "1001695358795"]


def get_personal_stat(mode: str, chat_id: str, most_common: int):
    data = {}
    with open("data.json", 'r') as data_file:
        data = json.load(data_file)  # type: dict
    count = Counter()
    for student in data.values():  # type: dict
        count[student["full_name"]] = student["messages"].get(chat_id, {mode: 0})[mode]
    if (most_common != 0):
        zipped_data = count.most_common(most_common)
    else:
        zipped_data = count.most_common()
    labels, values = zip(*zipped_data)
    position = np.arange(len(labels))

    fig, ax = plt.subplots()

    ax.bar_label(ax.barh(position, values))

    ax.set_yticks(position)

    labels = ax.set_yticklabels(labels)

    fig.set_figwidth(22)
    fig.set_figheight(15)
    ax.set_ylabel(mode + ' messages', fontsize='xx-large')
    ax.set_title("Personal stat at " + chat_id, fontsize='xx-large')
    plt.show()


def get_group_stat(mode: str, chat_id: str):
    data = {}
    with open("data.json", 'r') as data_file:
        data = json.load(data_file)  # type: dict
    count_group = Counter()
    for student in data.values():  # type: dict
        count_group[student["group"]] += student["messages"].get(chat_id, {mode: 0})[mode]
    print(count_group)
    labels = sorted(list(count_group.keys()))
    values = [count_group[labels[i]] for i in range(len(labels))]
    position = np.arange(len(labels))
    fig, ax = plt.subplots()
    ax.bar_label(ax.barh(position, values))
    ax.set_yticks(position)
    ax.set_yticklabels(labels)
    ax.set_xlabel(mode + 'messages')
    ax.set_title("Group stat at " + chat_id)
    plt.show()


def get_avg_msg_stat(mode: str, chat_ids: list, groups: list):
    data = {}
    with open("data.json", 'r') as data_file:
        data = json.load(data_file)  # type: dict
    students_data = {}
    with open("students_data.json", 'r') as data_file:
        students_data = json.load(data_file)  # type: dict
    msg_with_scholarship = []
    avg_with_scholarship = []
    msg_without_scholarship = []
    avg_without_scholarship = []
    msg_with_fx = []
    avg_with_fx = []
    for student in students_data.keys():
        if students_data[student]["group"] not in groups:
            continue
        for student_tg_data in data.values():
            if student == student_tg_data["full_name"]:
                msg = 0
                for chat_id in chat_ids:
                    msg += student_tg_data["messages"].get(chat_id, {mode: 0})[mode]
                if (students_data[student]["type"] in ['0', '1']):
                    msg_with_scholarship.append(msg)
                    avg_with_scholarship.append(students_data[student]["avg"])
                elif (students_data[student]["type"] == "2"):
                    msg_without_scholarship.append(msg)
                    avg_without_scholarship.append(students_data[student]["avg"])
                elif students_data[student]["type"] == '3':
                    msg_with_fx.append(msg)
                    avg_with_fx.append(students_data[student]["avg"])
                else:
                    print("Error: " + student)
    fig, ax = plt.subplots()
    ax.scatter(msg_with_scholarship, avg_with_scholarship, color='g')
    ax.scatter(msg_without_scholarship, avg_without_scholarship, color='y')
    ax.scatter(msg_with_fx, avg_with_fx, color='r')
    print(len(msg_with_fx) + len(msg_with_scholarship) + len(msg_without_scholarship))
    ax.set_title(str(groups) + " in " + "dialogs")
    ax.set_ylabel("Average score")
    ax.set_xlabel(mode + " messages")
    ax.set_xscale('log')
    plt.show()



if __name__ == "__main__":
    get_group_stat("count", "1001186169699")
    # get_personal_stat("length", "-1001566274537", 20)
    # get_personal_stat("count", "-1001566274537", 20)
    # get_avg_msg_stat("length", study_dialogs + flud_dialogs, ["M3138", "M3139"])