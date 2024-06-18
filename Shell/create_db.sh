#!/bin/bash

export HOME_DIR=/home/${USER}/Scripts/test_system
export SQL_DIR=/${HOME_DIR}/SQL
export PGPASSFILE=/home/${USER}/.pgpass

psql -h 7.7.7.77 -p 5432 -d my_test_framework -U postgres -f "${SQL_DIR}"/create_shemas.sql
psql -h 7.7.7.77 -p 5432 -d my_test_framework -U postgres -f "${SQL_DIR}"/create_tables.sql
psql -h 7.7.7.77 -p 5432 -d my_test_framework -U postgres -f "${SQL_DIR}"/create_procedures.sql