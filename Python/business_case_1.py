""" В этом кейсе создается структура в существующей базе данных (схема+таблица) """

import datetime
import json
import sys

sys.path.append('C:\\Users\\Всеволод\\PycharmProjects\\test_system\\home_project')

from home_project import psqlObjects, clsCalendar

test_db_2 = psqlObjects.PostgresConnect('test_db_2')
calendar_prod_2024 = clsCalendar.CalendarProd(2024)

""" создаем схемы и таблицы """
with open("C:\\Users\\Всеволод\\PycharmProjects\\test_system\\home_project\\CFG\\tables_config.json", "r", encoding="utf-8",
          errors="ignore") as json_f:
    tables_config: dict = json.load(json_f)

for schema in tables_config.keys():
    test_db_2.create_schema(schema=schema)
    for table_name in tables_config[schema].keys():
        test_db_2.create_table(schema=schema, table_name=table_name, tables_config=tables_config)

""" создаем хранимые процедуры """
with open("C:\\Users\\Всеволод\\PycharmProjects\\test_system\\home_project\\CFG\\procedure_config.json", "r",
          encoding="utf-8", errors="ignore") as json_f:
    procedure_config: dict = json.load(json_f)
for schema in procedure_config.keys():
    for procedure in procedure_config[schema].values():
        test_db_2.create_procedure(owner=schema, procedure=procedure)
