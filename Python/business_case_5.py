""" В этом кейсе производится выгрузка данных из базы данных в структуру json,
    чтобы в дальнейшем эти данными могли быть мигрированы в другую структуру другой базы данных """

import json
import sys

sys.path.append('C:\\Users\\Всеволод\\PycharmProjects\\test_system\\home_project')

from home_project import psqlObjects

my_finances = psqlObjects.PostgresConnect('my_finances')
my_finances.create_recovery_point()
