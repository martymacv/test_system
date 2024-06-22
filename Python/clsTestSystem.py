import datetime
import json


class TestSystemConf:
    def __init__(self, path_to_json_config):
        self.__path_to_json_config = path_to_json_config
        with open(path_to_json_config, "r", encoding="utf-8") as f:
            self.__actual_config = json.load(f)
        self.__new_path_to_json_config = None
        self.__new_config = None

    def get_actual_test_config(self):
        return self.__actual_config

    def get_new_test_config(self):
        return self.__new_config

    def create_new_test_config(self, new_json_config):
        self.__new_path_to_json_config = f"../CFG/test_config{datetime.datetime.now().strftime("%Y%m%d")}.json"
        self.__new_config = new_json_config
        with open(self.__new_path_to_json_config, "w", encoding="utf-8") as f:
            json.dump(self.__new_config, f, ensure_ascii=False, indent=2)
