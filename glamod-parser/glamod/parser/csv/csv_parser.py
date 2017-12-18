'''
Created on Dec 13, 2017

@author: William Tucker
'''

from glamod.parser.file_parser import FileParser


class CsvParser(FileParser):
    
    def parse(self, file, delimiter='|'):
        
        with open(file, encoding='iso-8859-1') as csv_file:
            
            header = csv_file.readline()
            columns = []
            column_index = 0
            for name in header.split(delimiter):
                
                column_name = name.strip()
                if not self._ignore_columns or not column_name in self._ignore_columns:
                    
                    if not self._table_constraints.is_column(column_name):
                        raise ValueError(
                            f"{column_name} is not a column of {self._table_constraints.name}")
                    
                    columns.append((column_index, column_name))
                
                column_index += 1
            
            for _, line in enumerate(csv_file):
                
                if line and line.strip() != '':
                    
                    row = {}
                    values = [value.strip() for value in line.split(delimiter)]
                    
                    for column_index, column_name in columns:
                        
                        value = values[column_index]
                        row[column_name] = self.parse_value(column_name, value)
                    
                    yield row
