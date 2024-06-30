d = {
    "DB_NAME": {
        "authorization": {
            "username": "username",
            "password": "password"
        },
        "DB_CONFIG": {
            "SCHEMA": {
                "TABLE_NAME": [],
                "NAME_TABLE": []
            }
        }
    }
}

print(d)
print(d["DB_NAME"]["DB_CONFIG"].items())

print(set([i for i in d["DB_NAME"]["DB_CONFIG"]]))
print(set([i for i in d["DB_NAME"]["DB_CONFIG"]["SCHEMA"]]))
