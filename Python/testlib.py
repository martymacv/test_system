import datetime
import json
import subprocess

import psycopg2


class LogIn:
    def __init__(self, db_name: str):
        self.__db_name = db_name
        with open("../CFG/db_properties.json", "r", encoding="utf-8", errors="ignore") as f:
            self.__db_properties = json.load(f)

    def get_username(self):
        return self.__db_properties[self.__db_name]["authorization"]["username"]

    def get_password(self):
        return self.__db_properties[self.__db_name]["authorization"]["password"]

    def get_host(self):
        return self.__db_properties[self.__db_name]["authorization"]["host"]

    def get_port(self):
        return self.__db_properties[self.__db_name]["authorization"]["port"]

    def get_dbname(self):
        return self.__db_properties

    def fetchall_from_db(self, sql_text):
        with psycopg2.connect(dbname=self.get_dbname(), host=self.get_host, user=self.get_username(),
                              password=self.get_password(), port=self.get_port()) as db_conn:
            with db_conn.cursor(sql_text) as cursor:
                return cursor.fetchall()


class TestModel(LogIn):
    def __init__(self, db_name: str):
        super().__init__(db_name)
        self.__test_config = dict()
        self.__file_config = subprocess.Popen(['bash', './find_recent_test_config.sh', f'{self.get_dbname()}'], subprocess.PIPE, text=True)
        if self.__file_config:
            with open(f"../CFG/{self.__file_config}", "r", encoding="utf-8", errors="ignore") as f:
                self.__test_config = json.load(f)
        else:
            sql_text = (f"select distinct schema, table_name"
                        f"  from aqa.release_table_list"
                        f" order by schema, table_name")
            self.__db_objects = self.fetchall_from_db(sql_text=sql_text)
            self.__test_config[self.get_dbname()] = dict()
            self.__test_config[self.get_dbname()]["DB_OBJECTS"] = dict()
            for schema in set(self.__db_objects[0]):
                self.__test_config[self.get_dbname()]["DB_OBJECTS"][schema] = dict()
            for schema, table in self.__db_objects:
                self.__test_config[self.get_dbname()]["DB_OBJECTS"][schema][table] = dict()
            with open(f"../CFG/test_config_{self.get_dbname()}_{datetime.datetime.now().strftime("%Y%m%d")}.json", "w", encoding="utf-8") as f:
                json.dump(self.__test_config, f, ensure_ascii=False, indent=2)

    def get_schemas_list(self):
        return sorted([schema for schema in self.__test_config[self.get_dbname()]["DB_OBJECTS"]])

    def get_tables_list(self, schema: str):
        return sorted([schema for schema in self.__test_config[self.get_dbname()]["DB_OBJECTS"][schema]])

    def get_db_object(self):
        return self.__db_objects


class TestPlan(TestModel):
    def __init__(self, db_name: str, schema: str):
        super().__init__(db_name)
        self.__schema = schema
        self.__test_plan = self.get_tables_list(schema)
        with open(f"../Logs/testrun_{self.get_dbname()}_{self.__schema}_{datetime.datetime.now().strftime("%Y%m%d%hh24%mi%ss")}.log", "w", encoding="utf-8") as log_f:
            log_f.writelines(self.__test_plan)

    def get_test_plan(self):
        return self.__test_plan

    def get_empty_check(self, table: str):
        return f"select count(*) from {self.__schema}.{table} and limit 1"


class TestReport(LogIn):
    def __init__(self, db_name: str):
        super().__init__(db_name)


