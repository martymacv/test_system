import json


class CalendarProd:
    def __init__(self, year: int):
        self.__year = year
        with open("C:\\Users\\Всеволод\\PycharmProjects\\test_system\\home_project\\CFG\\calendars_prod.json", "r", encoding="utf-8", errors="ignore") as json_f:
            self.__calendar_prod = json.load(json_f)

    def get_year(self):
        return self.__year

    def get_calendar_prod(self):
        return self.__calendar_prod

    def generate_date_list(self, day_type: str):
        """day_type = ['IS_HOLIDAY', 'IS_WORKDAY']"""
        date_list: str = "'''"
        for arg in [[f"{day:02}-{month:02}-{self.__year}" for day in days] for month, days in
                    self.__calendar_prod[day_type][str(self.__year)].items()]:
            date_list += "'',''".join(arg)
            date_list += "'',''"
        return date_list[:~2] + "'"
