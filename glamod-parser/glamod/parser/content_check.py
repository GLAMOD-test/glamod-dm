"""
Plan for generic content check:

1. Check column names are correct
2. In rules, define an instance of FieldCheck
3. Parse each record and cycle through FieldCheck instances

"""


from glamod.parser.field_check import FieldCheck


class _ContentCheck(object):

    def __init__(self, fpath):
        self.fpath = fpath


