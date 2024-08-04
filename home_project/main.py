from psqlObjects import *
from clsCalendar import *
# import NumPy
import random
import string


if __name__ == "__main__":
    # psql_db = PostgresConnect('my_finances')
    # calendar_prod = CalendarProd(2024)
    #
    # # psql_db.create_recovery_point()
    #
    # p_holiday_list = calendar_prod.generate_date_list("IS_HOLIDAY")
    # p_workday_list = calendar_prod.generate_date_list("IS_WORKDAY")
    # print(p_holiday_list)
    # print(p_workday_list)
    # # psql_db.execute_sql_script(f"call archive.calendar_date_generate(p_year => '{p_year}', p_holiday_list => {p_holiday_list}, p_workday_weekend_list => {p_workday_list})")
    #
    # # print(*psql_db.fetchall_from_db('select * from archive.income_hist'), sep='\n')
    # # "select case when count(*) = 0 then 0 else 1 end from :FIRST_TABLE: a left join :SECOND_TABLE b on a.:COLUMN_FROM_FIRST: = b.:COLUMN_FROM_SECOND"
    # # print(*psql_db.fetchall_from_db('select expense_id from archive.expenses_hist fetch first 1 rows only'), sep='\n')
    # # print(*psql_db.fetchall_from_db('select expense_id from current.expenses_base fetch first 1 rows only'), sep='\n')
    # print(*psql_db.fetchall_from_db(
    #     "select count(expense_id) from archive.expenses_hist where date_trunc('month', expense_date) = to_date('01-05-2024', 'dd-mm-yyyy hh24:mi:ss')"),
    #       sep='\n')
    # print(*psql_db.fetchall_from_db(
    #     "select count(expense_id) from current.expenses_base where date_trunc('month', expense_date) = to_date('01-05-2024', 'dd-mm-yyyy hh24:mi:ss')"),
    #       sep='\n')
    #
    # sql_text = """
    #     select case when count(*) = 0 then 1 else 0 end
    #       from ARCHIVE.EXPENSES_HIST a
    #       left join CURRENT.EXPENSES_BASE b on a.ARTICLE_ID = b.ARTICLE_ID and a.EXPENSE_DATE = b.EXPENSE_DATE
    #      where date_trunc('month', a.EXPENSE_DATE) = to_date('01-:MONTH:-2024', 'dd-mm-yyyy hh24:mi:ss') and b.EXPENSE_ID is null
    #     """
    # print(sql_text, sep='\n')
    # with open("CFG/tables_config.json", "r", encoding="utf-8", errors="ignore") as json_f:
    #     tables = json.load(json_f)

    # psql_db.create_table('TEST', 'CHECK_RESULT', tables=tables)

    # insert into table
    # data_in = {
    #     "ARTICLE_ID": 6,
    #     "PLAN_EXPENSE": 1000,
    #     "FACT_EXPENSE": 280+518+222,
    #     "EXPENSE_DATE": f"to_date('{'31-05-2024'}', 'dd-mm-yyyy')"
    # }
    # psql_db.insert_into_table('OP_ACT', 'EXPENSES', data_in)
    # data_in = {
    #     "CHECK_DESC": "'Сверка данных таблиц EXPENSES за выбранный период (МЕСЯЦ)'",
    #     "CHECK_SUITE": "'FULL_MATCH'",
    #     "SQL_TEXT": "'select case when count(*) = 0 then 1 else 0 end from ARCHIVE.EXPENSES_HIST a left join CURRENT.EXPENSES_BASE b on a.ARTICLE_ID = b.ARTICLE_ID and a.EXPENSE_DATE = b.EXPENSE_DATE where date_trunc(''month'', a.EXPENSE_DATE) = to_date(''01-:MONTH:-2024'', ''dd-mm-yyyy hh24:mi:ss'') and b.EXPENSE_ID is null'"
    # }
    # psql_db.insert_into_table('TEST', 'CHECK_SQL', data_in)

    # CREATE TABLE
    # with open("SQL/create_or_replace_functions.sql", "r", encoding="utf-8") as sql_f:
    #     sql_procedure = sql_f.read()
    #     print(sql_procedure)
    # print(psql_db.execute_sql_script(sql_procedure))

    # with open("SQL/ins_into_calendar_tbl.sql", "r", encoding="utf-8") as sql_f:
    #     sql_procedure = sql_f.read()
    #     print(sql_procedure)
    # print(psql_db.execute_sql_script(sql_procedure))

    sql_params = {"1": "1", "2": "1", "3": "1"}
    print(len(sql_params))

    def rotate_matrix90(mtrx: list, k: int = None):
        print(*[[row[i] for row in mtrx] for i in range(len(mtrx[0]))], sep='\n')

    matrix = [[0, 1, 2], [3, 4, 5]]
    print(*matrix, sep='\n')

    rotate_matrix90(matrix)


    def random_string(length):
        letters: list = []
        letters.extend('абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')
        print(''.join([letters[random.randint(0, len(letters) - 1)] for _ in range(length)]))

    print(random_string(10))
