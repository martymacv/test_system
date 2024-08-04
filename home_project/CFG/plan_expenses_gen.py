""" генератор json-структуры """

import json

with open("../DUMP/my_finances_data_dump_20240804.json", "r", encoding="utf-8", errors="ignore") as json_f:
    dump_data = json.load(json_f)

