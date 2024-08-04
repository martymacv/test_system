""" В этом кейса выполняются процедуры для автозаполнения таблиц """

import sys

sys.path.append('C:\\Users\\Всеволод\\PycharmProjects\\test_system\\home_project')

from home_project import psqlObjects, clsCalendar

db_conn = psqlObjects.PostgresConnect('test_db_2')
calendar_prod_2024 = clsCalendar.CalendarProd(2024)

is_holidays_day: str = calendar_prod_2024.generate_date_list("IS_HOLIDAY")
is_workdays_day: str = calendar_prod_2024.generate_date_list("IS_WORKDAY")

# заполняем производственный календарь за 2024 год
call_proc = f"call calc.ins_calendar_prod(p_year => '2024', p_holiday_list => {is_holidays_day}, p_workday_weekend_list => {is_workdays_day})"
db_conn.execute_sql_script(sql_text=call_proc)
