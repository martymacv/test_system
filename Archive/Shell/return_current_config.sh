#!/bin/bash

# shellcheck disable=SC2164
cd /home/"$USER"/Scripts/test_system/CFG
# shellcheck disable=SC2046
# shellcheck disable=SC2010
# shellcheck disable=SC2006
# shellcheck disable=SC2005
# shellcheck disable=SC2035
echo `ls *.json | grep "$1" | head -1`