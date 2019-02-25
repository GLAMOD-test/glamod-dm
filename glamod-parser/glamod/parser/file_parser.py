'''
Created on 01 Oct 2018

@author: Ag Stephens
'''

import logging
import pandas

from glamod.parser.settings import (INPUT_ENCODING, INPUT_DELIMITER, 
    VERBOSE_LOGGING, CHUNK_SIZE)


logger = logging.getLogger(__name__)


class FileParser(object):
    
    def __init__(self, fpath, delimiter=INPUT_DELIMITER, encoding=INPUT_ENCODING):
        self.fpath = fpath 
        self.delimiter = delimiter
        self.encoding = encoding
 
        self._fh = open(fpath, 'r', encoding=self.encoding)
        self._col_names = self._parse_header()


    def rewind(self, to_line=0):
        "Sets the seek position at the start of the file."
        self._fh.seek(0)

        if to_line > 0:
            for _ in range(to_line): 
                self._fh.readline() 


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
        df = pandas.read_csv(self._fh, encoding=self.encoding, 
                             delimiter=self.delimiter,
                             converters=convertors, usecols=columns,
                             skipinitialspace=True, verbose=VERBOSE_LOGGING)
        return df


    def read_chunks(self, convertors=None):
        
        self.rewind()
        chunk_reader = pandas.read_csv(self._fh, encoding=self.encoding,
                             delimiter=self.delimiter,
                             converters=convertors, skipinitialspace=True, 
                             verbose=VERBOSE_LOGGING, chunksize=CHUNK_SIZE)
        
        for chunk in chunk_reader:
            yield chunk


    def close(self):
        self._fh.close()

