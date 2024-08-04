""" В этом кейсе производится заполнение таблицы со статьями доходов/расходов """

import sys

sys.path.append('C:\\Users\\Всеволод\\PycharmProjects\\test_system\\home_project')

from home_project import psqlObjects

db_conn = psqlObjects.PostgresConnect('test_db_2')

# мне нужно в цикле заполнить статьи расходов и доходов, exit - значит выход из цикла
# datetime.datetime.strftime()
commands = {
    "exit": lambda: sys.exit(0)
}
command: str = ""
while command != "exit":
    row: str = input(f"Введите статью (символ (i)ncome/доход или (e)xpense/расход)\n и через запятую краткое название статьи: ")
    try:
        commands[row]()
    except KeyError:
        if row:  # and (isinstance(expense, int) or isinstance(expense, float)):
            print(row)
            data_in = {
                "article_type": f"'{row.split(',')[0].strip()}'",
                "article_desc": f"'{row.split(',')[1].strip()}'"
            }
            print(data_in)
            db_conn.insert_into_table(schema='calc', table_name='articles', params=data_in)
        else:
            print("no")