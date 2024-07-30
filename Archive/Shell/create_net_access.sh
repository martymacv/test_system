#!/bin/bash

# shellcheck disable=SC2164
cd /home/"$USER"
cp /home/"$USER"/Scripts/test_system/CFG/.pgpass .
chmod 600 .pgpass