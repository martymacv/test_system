import json
import sys

sys.path.append('C:\\Users\\Всеволод\\PycharmProjects\\test_system\\home_project')

from home_project import psqlObjects, clsTesting


test_db_2 = psqlObjects.PostgresConnect('test_db_2')
with open("C:\\Users\\Всеволод\\PycharmProjects\\test_system\\home_project\\CFG\\tables_config.json", "r",
          encoding="utf-8",
          errors="ignore") as json_f:
    tables_config: dict = json.load(json_f)

test_cases = clsTesting.BaseTestCases(db_name='test_db_2',
                                      test_schema='test',
                                      table_config=tables_config)

""" создаем базовые тесты """
for params in test_cases.generate_base_test_cases('CHECK_TABLES'):
    test_db_2.insert_into_table(schema='test', table_name='check_sql', params=params)
for params in test_cases.generate_base_test_cases('CHECK_COLUMNS'):
    test_db_2.insert_into_table(schema='test', table_name='check_sql', params=params)

""" запускаем тесты """
sql_text = "select check_id from test.check_sql where check_suite in ('CHECK_COLUMNS','CHECK_TABLES')"
for check_id in test_db_2.fetchall_from_db(sql_text=sql_text):
    call_proc = f"call test.run_check_sql(p_check_id => {check_id[0]}, p_check_date => to_date('28-07-2024', 'dd-mm-yyyy'))"
    test_db_2.execute_sql_script(sql_text=call_proc)
