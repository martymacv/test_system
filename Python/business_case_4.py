""" В этом кейсе реализован простой интерфейс командно строки, чтобы у пользователя
    была возможность вводить данные о своих расходах и реальных доходах """

import datetime
import sys

sys.path.append('C:\\Users\\Всеволод\\PycharmProjects\\test_system\\home_project')

from home_project import psqlObjects

db_conn = psqlObjects.PostgresConnect('my_finances')

# incomes
sql_text = f"select id, article from archive.articles where id >= 18"
incomes_list = db_conn.fetchall_from_db(sql_text=sql_text)
sql_text = f"select b.calendar_date, case when b.is_workday = true then 'workday' else 'weekend' end from current.incomes_base a right join archive.calendar b on a.income_date = b.calendar_date where b.calendar_date between to_date('01-05-2024', 'dd-mm-yyyy hh24:mi:ss') and now() and a.income_date is null order by b.calendar_date"
income_dates = db_conn.fetchall_from_db(sql_text=sql_text)
print(incomes_list)
print(income_dates)
# datetime.datetime.strftime()
for date in income_dates:
    for ndx, article in incomes_list:
        income: str = input(f"Введите доход по статье {article} за {date[0].strftime('%d-%m-%Y')} ({date[1]}): ")
        if income:  # and (isinstance(expense, int) or isinstance(expense, float)):
            print(income)
            data_in = {
                "income_id": f"'{article}'",
                "incomes": f"{income}",
                "income_date": f"to_date('{date[0].strftime('%d-%m-%Y')}', 'dd-mm-yyyy')"
            }
            print(data_in)
            db_conn.insert_into_table(schema='current', table_name='incomes_base', params=data_in)
        else:
            print("no")
# expenses
sql_text = f"select id, article from archive.articles where id < 18"
expenses_list = db_conn.fetchall_from_db(sql_text=sql_text)
sql_text = f"select b.calendar_date, case when b.is_workday = true then 'workday' else 'weekend' end from current.expenses_base a right join archive.calendar b on a.expense_date = b.calendar_date where b.calendar_date between to_date('01-05-2024', 'dd-mm-yyyy hh24:mi:ss') and now() and a.expense_date is null order by b.calendar_date"
expense_dates = db_conn.fetchall_from_db(sql_text=sql_text)
print(expenses_list)
print(expense_dates)
# datetime.datetime.strftime()
for date in expense_dates:
    for ndx, article in expenses_list:
        expense: str = input(f"Введите расход по статье {article} за {date[0].strftime('%d-%m-%Y')} ({date[1]}): ")
        if expense:  # and (isinstance(expense, int) or isinstance(expense, float)):
            print(expense)
            data_in = {
                "article_id": f"{ndx}",
                "plan_expense": f"0",
                "fact_expense": f"{expense}",
                "expense_date": f"to_date('{date[0].strftime('%d-%m-%Y')}', 'dd-mm-yyyy')"
            }
            print(data_in)
            db_conn.insert_into_table(schema='current', table_name='expenses_base', params=data_in)
        else:
            print("no")
# def insert_income(summa: int, article_id: int):
#     pass

# для начала нужно выбрать, что мы вводим, нужен список команд
# commands = {
#     "help": lambda: print("Здесь должен быть список досутпных команд"),
#     "incomes": lambda: input("Введите сумму реального дохода и статью дохода через запятую: "),
#     "expenses": "expenses",
#     "exit": lambda: sys.exit(0)
# }
# print("Введите команду, что хотите сделать:")
# command: str = ""
# while command != "exit":
#     command = input("Введите команду, что хотите сделать: ")
#     res = commands[command]()
#     print(res.split(','))
# data_in = {
#                 "SCHEMA": f"'{row[0]}'",
#                 "OBJ_NAME": f"'{row[1]}'",
#                 "CHECK_DESC": f"'Базовая проверка объекта {row[0]}.{row[1]}'",
#                 "CHECK_SUITE": f"'{tc_type.upper()}'",
#                 "SQL_TEXT": f"'{sql_text}'"
#             }
