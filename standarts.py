import json


def get_table_list(owner):
    with open('table_list.json', 'r') as j_data:
        return json.load(j_data)[owner]


def set_table_list(table_dict):
    with open('table_list.json', 'w+') as j_data:
        json.dump(table_dict, j_data, indent=4, encoding='utf-8')
