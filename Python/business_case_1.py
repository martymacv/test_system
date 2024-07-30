import json
import sys

sys.path.append('C:\\Users\\Всеволод\\PycharmProjects\\test_system\\psql_developer')

from psql_developer import psqlObjects, clsCalendar

""" В этом кейсе создается структура в существующей базе данных (схема+таблица)
    Наполняется генерируемыми данными: тестовые сценарии для пустых таблиц и заполнение календаря """

test_db_2 = psqlObjects.PostgresConnect('test_db_2')
calendar_prod_2024 = clsCalendar.CalendarProd(2024)

""" создаем схемы и таблицы """
with open("C:/Users/Всеволод/PycharmProjects/test_system/psql_developer/CFG/tables_config.json", "r", encoding="utf-8",
          errors="ignore") as json_f:
    tables_config: dict = json.load(json_f)
for schema in tables_config.keys():
    test_db_2.create_schema(schema=schema)
    for table_name in tables_config[schema].keys():
        test_db_2.create_table(schema=schema, table_name=table_name, tables_config=tables_config)

""" создаем хранимые процедуры """
with open("C:/Users/Всеволод/PycharmProjects/test_system/psql_developer/CFG/procedure_config.json", "r",
          encoding="utf-8", errors="ignore") as json_f:
    procedure_config: dict = json.load(json_f)
for schema in procedure_config.keys():
    for procedure in procedure_config[schema].values():
        test_db_2.create_procedure(owner=schema, procedure=procedure)

""" создаем базовые тесты """
columns_in_config: str = ""
columns_in_db: str = ""
for schema in tables_config.keys():
    for table, columns in tables_config[schema].items():
        columns_in_config = ",".join(columns).lower()
        data_in = {
            "SCHEMA": f"'{schema}'",
            "OBJ_NAME": f"'{table}'",
            "CHECK_DESC": f"'Сверка полей в таблице {schema}.{table}'",
            "CHECK_SUITE": "'CHECK_COLUMNS'",
            "SQL_TEXT": f"'select case when array_to_string(array_agg(COLUMN_NAME), '','') = ''{columns_in_config}'' then 1 else 0 end from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME = ''{table}'' and TABLE_SCHEMA = ''{schema}'''"
        }
        test_db_2.insert_into_table('test', 'check_sql', data_in)

is_holidays_day: str = calendar_prod_2024.generate_date_list("IS_HOLIDAY")
is_workdays_day: str = calendar_prod_2024.generate_date_list("IS_WORKDAY")
for column_name in tables_config["calc"]["calendar"].keys():
    print(column_name)
    data_in = {
        "SCHEMA": "'calc'",
        "OBJ_NAME": "'calendar'",
        "CHECK_DESC": f"'Проверка данных calc.calendar'",
        "CHECK_SUITE": "'CHECK_NOT_NULL'",
        "SQL_TEXT": f"'select count({column_name.upper()}) from CALC.CALENDAR where CALENDAR_DATE between to_date(''01-01-:YEAR:'', ''dd-mm-yyyy hh24:mi:ss'') and to_date(''31-12-:YEAR:'', ''dd-mm-yyyy hh24:mi:ss'') and {column_name.upper()} is not null'"
    }
    test_db_2.insert_into_table('test', 'check_sql', data_in)

""" выполняем процедуры """
call_proc = f"call calc.ins_calendar_prod(p_year => '{calendar_prod_2024.get_year()}'\
                                         ,p_holiday_list => {is_holidays_day}\
                                         ,p_workday_weekend_list => {is_workdays_day})"
test_db_2.execute_sql_script(sql_text=call_proc)

sql_text = "select check_id from test.check_sql where check_suite in ('CHECK_COLUMNS','CHECK_NOT_NULL')"
for check_id in test_db_2.fetchall_from_db(sql_text=sql_text):
    call_proc = f"call test.run_check_sql(p_check_id => {check_id[0]})"
    test_db_2.execute_sql_script(sql_text=call_proc)
