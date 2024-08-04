import json
import sys
import datetime

sys.path.append('C:\\Users\\Всеволод\\PycharmProjects\\test_system\\home_project')

from home_project import psqlObjects, clsTesting

test_db_2 = psqlObjects.PostgresConnect('test_db_2')