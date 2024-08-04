import datetime
import decimal
import json

import psycopg2


def convert_type_to_json(data_dump: list):
    dump_base = list()
    for row in data_dump:
        dump_2nd = list()
        for field in row:
            if isinstance(field, decimal.Decimal):
                dump_2nd.append(float(field))
            elif isinstance(field, datetime.date):
                dump_2nd.append(str(field))
            elif isinstance(field, str):
                dump_2nd.append("''".join(field.split("'")))
            else:
                dump_2nd.append(field)
        dump_base.append(dump_2nd)
    return dump_base


class PostgresConnect:
    def __init__(self, dbname: str):  # , host: str, user: str, password: str, port: int):
        self.dbname = dbname
        self.autologin_params = dict()
        with open("C:\\Users\\Всеволод\\PycharmProjects\\test_system\\home_project\\CFG\\.pgpass", "r", encoding="utf-8", errors="ignore") as pgpass_f:
            for db_p in [db_params.split(":") for db_params in pgpass_f.read().split("\n")]:
                self.autologin_params.setdefault(db_p[2])
                self.autologin_params[db_p[2]] = db_p[:2] + db_p[3:]
        self.host = self.autologin_params[self.dbname][0]
        self.port = self.autologin_params[self.dbname][1]
        self.user = self.autologin_params[self.dbname][2]
        self.password = self.autologin_params[self.dbname][3]
        """ в json формате гораздо удобнее хранить, так как сразу можно сохранить в dict(),
            но .pgpass является стандартным хранилищем паролей для системы Posgtresql """
        # with open("../CFG/db_configs.json", "r", encoding="utf-8", errors="ignore") as json_f:
        #     self.autologin_params = json.load(json_f)
        # self.host = self.autologin_params[self.dbname]["host"]
        # self.port = self.autologin_params[self.dbname]["port"]
        # self.user = self.autologin_params[self.dbname]["user"]
        # self.password = self.autologin_params[self.dbname]["password"]

    def get_autologin_params(self):
        return self.autologin_params

    def call_db_proc(self, proc_name: str, proc_params: list):
        with psycopg2.connect(dbname=self.dbname, host=self.host, user=self.user,
                              password=self.password, port=self.port) as db_conn:
            with db_conn.cursor() as cursor:
                cursor.callproc(proc_name, proc_params)
                # return cursor.fetchall()

    def execute_sql_script(self, sql_text):
        with psycopg2.connect(dbname=self.dbname, host=self.host, user=self.user,
                              password=self.password, port=self.port) as db_conn:
            db_conn.set_session(autocommit=True)
            with db_conn.cursor() as cursor:
                cursor.execute(sql_text)
                cursor.execute('COMMIT')

    def fetchall_from_db(self, sql_text):
        with psycopg2.connect(dbname=self.dbname, host=self.host, user=self.user,
                              password=self.password, port=self.port) as db_conn:
            db_conn.set_session(autocommit=True)
            with db_conn.cursor() as cursor:
                cursor.execute(sql_text)
                return cursor.fetchall()

    def create_schema(self, schema: str):
        sql_text = f"CREATE SCHEMA IF NOT EXISTS {schema}"
        self.execute_sql_script(sql_text=sql_text)

    def create_table(self, schema: str, table_name: str, tables_config: dict):
        columns = ""
        comments = ""
        for column_name in tables_config[schema][table_name].keys():
            columns += f"    {column_name} {tables_config[schema][table_name][column_name]["data_type"]},\n"
        columns = columns[:~1]
        for column_name in tables_config[schema][table_name].keys():
            comments += f"COMMENT ON COLUMN {schema}.{table_name}.{column_name} IS '{tables_config[schema][table_name][column_name]["comment"]}';\n"
        sql_text = f"CREATE TABLE IF NOT EXISTS {schema}.{table_name} (\n{columns});\n\n{comments}"
        # print(sql_text)
        self.execute_sql_script(sql_text=sql_text)

    def create_procedure(self, owner: str, procedure: str):
        with open(procedure, "r", encoding="utf-8", errors="ignore") as sql_f:
            procedure_code: str = sql_f.read()
            procedure_code: str = procedure_code.replace(':OWNER:', owner)
            print(procedure_code)
            self.execute_sql_script(sql_text=procedure_code)

    def insert_into_table(self, schema: str, table_name: str, params: dict):
        data_in = ""
        for column_name in params.keys():
            data_in += f"{column_name},"
        data_in = '(' + data_in[:~0] + ')' + ' SELECT '
        for value in params.values():
            data_in += f"{value},"
        data_in = data_in[:~0]
        sql_text = f"INSERT INTO {schema}.{table_name} {data_in}"
        print(sql_text)
        self.execute_sql_script(sql_text=sql_text)

    def create_recovery_point(self):
        dump = dict()
        sql_text = f"select NSPNAME from PG_CATALOG.PG_NAMESPACE where NSPNAME not in ('pg_toast','pg_catalog','public','information_schema')"
        for schema in self.fetchall_from_db(sql_text=sql_text):
            dump[schema[0]] = dict()
            sql_text = f"select TABLE_NAME from INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA = '{schema[0]}' and TABLE_NAME not like 'v_%'"
            for table in self.fetchall_from_db(sql_text=sql_text):
                dump[schema[0]][table[0]] = dict()
                # dump[schema[0]][table[0]]["columns"] = None
                dump[schema[0]][table[0]]["values"] = list()
                sql_text = f"select array_to_string(array_agg(COLUMN_NAME), ',') from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME = '{table[0]}' and TABLE_SCHEMA = '{schema[0]}'"
                columns = self.fetchall_from_db(sql_text=sql_text)[0][0].split(',')
                sql_text = f"select * from {schema[0]}.{table[0]}"
                dump_base = convert_type_to_json(self.fetchall_from_db(sql_text=sql_text))
                for row in dump_base:
                    dump[schema[0]][table[0]]["values"].append(dict(zip(columns, row)))
        with open(f"C:\\Users\\Всеволод\\PycharmProjects\\test_system\\home_project\\DUMP\\{self.dbname}_data_dump_{datetime.datetime.now().strftime("%Y%m%d")}.json", "w",
                  encoding="utf-8") as json_f:
            json.dump(dump, json_f, indent=2, ensure_ascii=False)

    def recovery_data_in_db(self, tables_recovery: dict):
        pass

    def migrate_db_from_old_to_new(self):
        """ данная миграция выполняется между БД, у которых отличается структура данных """
        pass

    def test_return(self):
        print(self.autologin_params)

# test = PostgresConnect("my_finances")
# test.test_return()
# with open("SQL/create_or_replace_functions.sql", "r", encoding="utf-8") as sql_f:
#     sql_procedure = sql_f.read()
#     print(sql_procedure)
# print(test.execute_sql_script(sql_procedure))


# class CmdInterface(PostgresConnect):
#     def __init__(self, dbname: str):
#         super().__init__(dbname)
#
#     def ins_new_expen