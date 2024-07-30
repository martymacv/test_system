import sys

sys.path.append('C:\\Users\\Всеволод\\PycharmProjects\\test_system\\psql_developer')

from psql_developer import psqlObjects

test_db_2 = psqlObjects.PostgresConnect('test_db_2')

sql_text = "select check_id from test.check_sql where check_suite in ('CHECK_COLUMNS','CHECK_NOT_NULL')"
for check_id in test_db_2.fetchall_from_db(sql_text=sql_text):
    call_proc = f"call test.run_check_sql(p_check_id => {check_id[0]}, p_check_date => to_date('28-07-2024', 'dd-mm-yyyy'))"
    test_db_2.execute_sql_script(sql_text=call_proc)
