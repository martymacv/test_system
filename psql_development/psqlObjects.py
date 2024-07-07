import json

import psycopg2


class PostgresConnect:
    def __init__(self, dbname: str):  # , host: str, user: str, password: str, port: int):
        self.dbname = dbname
        self.autologin_params = dict()
        with open("../CFG/.pgpass", "r", encoding="utf-8", errors="ignore") as pgpass_f:
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

    def fetchall_from_db(self, sql_text):
        with psycopg2.connect(dbname=self.dbname, host=self.host, user=self.user,
                              password=self.password, port=self.port) as db_conn:
            with db_conn.cursor() as cursor:
                cursor.execute(sql_text)
                return cursor.fetchall()

    def test_return(self):
        print(self.autologin_params)


test = PostgresConnect("my_finances")
test.test_return()
print(test.fetchall_from_db("select * from ei.calendar"))
