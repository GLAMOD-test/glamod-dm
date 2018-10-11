'''
Created on 01 Oct 2018

@author: Ag Stephens
'''

import pandas


from glamod.parser.exceptions import ParserError
from glamod.parser.settings import INPUT_ENCODING, INPUT_DELIMITER, VERBOSE_LOGGING


class FileParser(object):
    
    def __init__(self, fpath, delimiter=INPUT_DELIMITER, encoding=INPUT_ENCODING):
        self.fpath = fpath 
        self.delimiter = delimiter

        self._fh = open(fpath, 'r', encoding=encoding)
        self._col_names = self._parse_header()


    def rewind(self):
        "Sets the seek position at the start of the file."
        self._fh.seek(0)


    def _parse_header(self):
        assert(self._fh.tell() == 0)
        return self.readline()


    def readline(self):
        "Reads next line and splits on delimiter."
        return [_.strip() for _ in self._fh.readline().rstrip().split(self.delimiter)]         


    def get_column_names(self):
        return self._col_names


    def get_subset_dataframe(self, convertors=None, columns=None):
        self.rewind()
        df = pandas.read_csv(self._fh, encoding=INPUT_ENCODING, 
                             delimiter=INPUT_DELIMITER,
                             converters=convertors, usecols=columns,
                             skipinitialspace=True, verbose=VERBOSE_LOGGING)
        return df


    def close(self):
        self._fh.close()

