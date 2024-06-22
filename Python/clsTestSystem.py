import datetime
import json


class TestSystemConf:
    def __init__(self, config=None):
        self.__current_config = config

    def read_from_json_config(self, path_to_json_config):
        with open(path_to_json_config, "r", encoding="utf-8") as f:
            self.__current_config = json.load(f)

    def write_to_json_config(self, path_to_json_config):
        with open(path_to_json_config, "w", encoding="utf-8") as f:
            json.dump(self.__current_config, f, ensure_ascii=False, indent=2)

    def get_actual_test_config(self):
        return self.__current_config

    def create_test_system_image(self,
                                 uni_owner_list: set,
                                 database_name_list: set,
                                 tables_list: list[tuple],
                                 authorization_list: list[tuple]):
        for owner in uni_owner_list:
            self.__current_config[owner] = dict()
        for owner, table in tables_list:
            self.__current_config[owner][table] = dict()
            self.__current_config[owner][table]["full_check_list"] = []
            self.__current_config[owner][table]["pass_check_list"] = []
            self.__current_config[owner][table]["fail_check_list"] = []
            self.__current_config[owner][table]["skip_check_list"] = []
            self.__current_config[owner][table]["null_check_list"] = []
            self.__current_config[owner][table]["quarantine_check_list"] = []
            self.__current_config[owner][table]["other_check_list"] = []
            self.__current_config["properties"] = dict()
        for database_name in database_name_list:
            self.__current_config["properties"][database_name] = dict()
        for database_name, user, password in authorization_list:
            self.__current_config["properties"][database_name][user] = ""
            self.__current_config["properties"][database_name][password] = ""
        return self.__current_config

    def get_full_check_list(self, owner, table):
        return self.__current_config[owner][table]["full_check_list"]

    def get_pass_check_list(self, owner, table):
        return self.__current_config[owner][table]["pass_check_list"]

    def get_fail_check_list(self, owner, table):
        return self.__current_config[owner][table]["fail_check_list"]

    def get_skip_check_list(self, owner, table):
        return self.__current_config[owner][table]["skip_check_list"]

    def get_null_check_list(self, owner, table):
        return self.__current_config[owner][table]["null_check_list"]

    def get_quarantine_check_list(self, owner, table):
        return self.__current_config[owner][table]["quarantine_check_list"]

    def get_other_check_list(self, owner, table):
        return self.__current_config[owner][table]["other_check_list"]
