
from glamod.parser.rules import HeaderTableParserRules


def test_HeaderTableParserRules_are_consistent():
    x = HeaderTableParserRules()
    assert(len(x.extended_fields) == 0)

    vlookupd1, vlookupd2 = x.vlookup_fields.values()

    vlookup1 = set(list(vlookupd1.keys()))
    vlookup2 = set(list(vlookupd2.keys()))
    assert( vlookup1.intersection(vlookup2) == set())

    fields = set(list(x.fields.keys()))

    assert( vlookup1.intersection(fields) == set())
    assert( vlookup2.intersection(fields) == set())