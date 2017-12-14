'''
Created on Dec 13, 2017

@author: vagrant
'''

from parse.parser import Parser

class CsvParser(Parser):
    
    def parse(self, file, delimiter='|'):
        
        with open(file, encoding='iso-8859-1') as csv_file:
            
            columns = [line.strip() for line in csv_file.readline().split(delimiter)]
            for column_name in columns:
                
                if not self._table_constraints.is_column(column_name):
                    raise ValueError(
                        f"{column_name} is not a column of {self._table_constraints.name}")
            
            rows = []
            for _, line in enumerate(csv_file):
                
                row = {}
                values = [line.strip() for line in csv_file.readline().split(delimiter)]
                
                for i in range(0, len(columns)):
                    
                    column_name = columns[i]
                    value = values[i]
                    
                    row[column_name] = self.parse_value(column_name, value)
            
            rows.append(row)
        
        return rows
