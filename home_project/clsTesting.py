import datetime
import json
import random

from psqlObjects import PostgresConnect


def convert_table_config_to_list(table_config: dict, len_list: int):
    config_list: list = []
    for schema_name in table_config.keys():
        for table_name in table_config[schema_name].keys():
            for column_name in table_config[schema_name][table_name].keys():
                for param in table_config[schema_name][table_name][column_name].keys():
                    row = [schema_name, table_name, column_name, param][:len_list]
                    if row not in config_list:
                        config_list.append(row)
    return config_list


class TestCase:
    def __init__(self, db_name: str, test_schema: str):
        self.__db_name = db_name
        self.__test_schema = test_schema

    def get_db_name(self):
        return self.__db_name

    def get_test_schema(self):
        return self.__test_schema

    def set_db_name(self, db_name: str):
        self.__db_name = db_name

    def set_test_schema(self, test_schema: str):
        self.__test_schema = test_schema


class BaseTestCases(TestCase):
    def __init__(self, db_name: str, test_schema: str, table_config: dict):
        super().__init__(db_name, test_schema)
        self.__table_config = table_config
        with open("C:\\Users\\Всеволод\\PycharmProjects\\test_system\\home_project\\CFG\\base_test_cases.json", "r",
                  encoding="utf-8", errors="ignore") as json_f:
            self.__base_test_cases = json.load(json_f)

    def generate_base_test_cases(self, tc_type: str):
        """ tc_type = 'CHECK_TABLES' [ | 'CHECK_COLUMNS' ] """
        test_cases: list = []
        sql_params: list = self.__base_test_cases[tc_type]['sql_params']
        for row in convert_table_config_to_list(table_config=self.__table_config,
                                                len_list=len(self.__base_test_cases[tc_type]['sql_params'])):
            sql_text: str = self.__base_test_cases[tc_type]['sql_text']
            for param, value in dict(zip(sql_params, row)).items():
                sql_text = sql_text.replace(param, value)
            print(sql_text)
            data_in = {
                "SCHEMA": f"'{row[0]}'",
                "OBJ_NAME": f"'{row[1]}'",
                "CHECK_DESC": f"'Базовая проверка объекта {row[0]}.{row[1]}'",
                "CHECK_SUITE": f"'{tc_type.upper()}'",
                "SQL_TEXT": f"'{sql_text}'"
            }
            test_cases.append(data_in)
        return test_cases


class RecoveryTestCases(TestCase):
    def __init__(self, db_name: str, test_schema: str, last_dump_date: datetime.date):
        super().__init__(db_name, test_schema)
        self.__last_dump_date = last_dump_date
        # self.test_attr = json.loads(self.__base_test_cases)
        # with open(f"./DUMP/{self.__db_name}_data_dump_{self.__last_dump_date.strftime('%Y%m%d')}.json", "r", encoding="utf-8", errors="ignore") as json_f:
        #     self.__dump_test_cases = json.load(json_f)[self.__test_schema]


def generate_data(data_type: str, quantity_rows: int, max_length: int):
    test_data: list = list()
    data_logs: set = set()
    n = 0
    if data_type == 'numeric':
        while n < quantity_rows:
            data_logs.add(str(random.randint(0, 2**max_length)))
            n = len(data_logs)
        test_data = list(data_logs)
    elif data_type == 'boolean':
        booleans: list = ["'true'", "'false'"]
        for _ in range(quantity_rows):
            test_data.append(booleans[random.randint(0, 1)])
    elif data_type == 'timestamp without time zone':
        for _ in range(quantity_rows):
            test_data.append(f"to_timestamp('{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}', 'yyyy-mm-dd hh24:mi:ss.ff6')")
    elif data_type == 'date':
        while n < quantity_rows:
            data_logs.add(f"to_date('{random.randint(2000, 2099)}-{random.randint(1, 12):02}-{random.randint(1, 28):02}', 'yyyy-mm-dd')")
            n = len(data_logs)
        test_data = list(data_logs)
    elif data_type == 'character varying':
        letters: list = []
        letters.extend('абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')
        while n < quantity_rows:
            data_logs.add(f"'{''.join([letters[random.randint(0, len(letters) - 1)] for _ in range(max_length)])}'")
            n = len(data_logs)
        test_data = list(data_logs)
    return test_data


class TestData(PostgresConnect):
    def __init__(self, dbname: str, schema_name: str, table_name: str):
        super().__init__(dbname)
        self.__schema_name: str = schema_name
        self.__table_name: str = table_name
        sql_text = f"select column_name, data_type, case when character_maximum_length is not null then character_maximum_length else\
                                                    case when numeric_precision_radix is not null then numeric_precision_radix else datetime_precision end end as precision from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME = '{table_name}' and TABLE_SCHEMA = '{schema_name}' and COLUMN_DEFAULT is null"
        self.__column_list: list = self.fetchall_from_db(sql_text=sql_text)
        self.__data_types: list = self.fetchall_from_db(sql_text=sql_text)
        print(self.__data_types)

    def get_column_list(self):
        return self.__column_list

    def ins_test_data(self, quantity_rows: int):
        column_list = [pos[0] for pos in self.get_column_list()]
        data_type_list = [pos[1:] for pos in self.get_column_list()]
        test_data_list: list = []
        # max_length = [pos[2] for pos in self.get_column_list()]
        sql_params: list = []
        for data_type, max_length in data_type_list:
            test_data_list.append(generate_data(data_type, quantity_rows, max_length=max_length))
        print(test_data_list)
        row_around = [[row[i] for row in test_data_list] for i in range(len(test_data_list[0]))]
        for data_row in row_around:
            sql_text = f"INSERT INTO {self.__schema_name}.{self.__table_name} ({','.join(column_list)}) SELECT {','.join(data_row)}"
            self.execute_sql_script(sql_text=sql_text)
        # return sql_text


# with open("C:\\Users\\Всеволод\\PycharmProjects\\test_system\\home_project\\CFG\\tables_config.json", "r", encoding="utf-8",
#           errors="ignore") as json_f:
#     tables_config: dict = json.load(json_f)
#
# for schema_name in tables_config.keys():
#     for table_name in tables_config[schema_name].keys():
#         TestData('test_db_2', schema_name, table_name).ins_test_data(10)
# testcase = TestData('test_db_2', 'fact', 'expenses')
# print(testcase.ins_test_data(1000))
