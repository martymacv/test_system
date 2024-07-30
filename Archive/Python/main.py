import sys

import testlib

if __name__ == '__main__':
    """Здесь мы запускаем TestRun"""
    testrun = testlib.TestReport(sys.argv[1], sys.argv[2])

    for table in testrun.get_test_plan():
        testrun.get_empty_check(table=table)
