'''
Created on Nov 28, 2017

@author: William Tucker
'''

import argparse

from db.db_manager import DBManager
from db.table_constraints import TableConstraints

from parse.csv.csv_parser import CsvParser


CONNECTION_STRING = 'postgresql://glamod:glamod@localhost:5432/c3s_311a_dev'
SCHEMA = 'cdm_v1'


def load_model(data_file, table_name, db_manager):
    
    model_class = db_manager.get_model_class(table_name)
    table = db_manager.get_table(table_name)
    
    constraints = TableConstraints(table)
    parser = CsvParser(constraints)
    parsed_entries = parser.parse(data_file)
    
    db_manager.start_session()
    for entry in parsed_entries:
        db_manager.merge(model_class(**entry))
    
    db_manager.commit()
    db_manager.close_session()

def main():
    
    parser = argparse.ArgumentParser(description='Loads data from an XLSX file.')
    parser.add_argument('file', metavar='f', type=str,
                        help='the name of the file to parse')
    parser.add_argument('table', metavar='t', type=str,
                        help='the name of the table that the data belongs to')
    
    args = parser.parse_args()
    
    db_manager = DBManager(CONNECTION_STRING, SCHEMA)
    
    file_name = args.file
    table_name = args.table
    
    load_model(file_name, table_name, db_manager)
