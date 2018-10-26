from glamod.parser.convertors import *


def test_list_of_ints():
    assert (list_of_ints('  2,3 ') == [2, 3])
    assert (list_of_ints(' ') == [])

    bad_tests = ['2 2 2', '3, , 5']

    class _TestParserException(Exception):
        pass

    for _bt in bad_tests:
        try:
            list_of_ints(_bt)
            raise _TestParserException()
        except ValueError as err:
            pass

