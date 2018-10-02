'''
Created on 01 Oct 2018

@author: Ag Stephens
'''

from glamod.parser.exceptions import ParserError
from glamod.parser.settings import INPUT_ENCODING


class FileParser(object):
    
    def __init__(self, fpath, delimiter='|'):
        self.fpath = fpath 
        self.delimiter = delimiter

        self._fh = open(fpath, 'r', encoding=INPUT_ENCODING)
        self._col_names = self._parse_header()


    def _parse_header(self):
        assert(self._fh.tell() == 0)
        return self.readline()   


    def readline(self):
        "Reads next line and splits on delimiter."
        return self._fh.readline().rstrip().split(self.delimiter)         


    def get_column_names(self):
        return self._col_names        

      
    def parse(self, file, delimiter='|', ignore_columns=None, ignore_strict=False):
        
        with open(file, encoding='iso-8859-1') as csv_file:
            
            header = csv_file.readline()
            columns = []
            column_index = 0
            for name in header.split(delimiter):
                
                column_name = name.strip()
                if not ignore_columns or not column_name in ignore_columns:
                    
                    if not self._table_constraints.is_column(column_name):
                        raise ValueError(
                            f"'{column_name}' is not a column of {self._table_constraints.name}")
                    
                    columns.append((column_index, column_name))
                
                column_index += 1
            
            if ignore_strict and ignore_columns:
                
                _, column_names = zip(*columns)
                for ignore_column in ignore_columns:
                    if not ignore_column in column_names:
                        raise ValueError(f"'{ignore_column}' column from ignore list not "
                                         "present in file. Use ignore_strict=False to disable")
            
            for line_index, line in enumerate(csv_file):
                
                line_num = line_index + 2
                
                if line and line.strip() != '':
                    
                    row = {}
                    values = [value.strip() for value in line.split(delimiter)]
                    
                    for column_index, column_name in columns:
                        
                        value = values[column_index]
                        
                        try:
                            row[column_name] = self.parse_value(column_name, value)
                        except ParserError as e:
                            import sys
                            raise type(e)(
                                str(e) + f" at line {line_num}").with_traceback(
                                    sys.exc_info()[2])
                    
                    yield row
