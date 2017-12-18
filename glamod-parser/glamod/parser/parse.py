'''
Created on Nov 28, 2017

@author: William Tucker
'''

import argparse

from getpass import getpass

from glamod.db.db_manager import DBManager
from glamod.db.table_constraints import TableConstraints

from glamod.parser.csv.csv_parser import CsvParser
from glamod.parser.xlsx.xlsx_parser import XlsxParser


CONNECTION_TEMPLATE = 'postgresql://{user}:{password}@{host}:{port}/{database}'


def load_model(data_file, table_name, db_info, parser_class=CsvParser):
    
    connection_string = CONNECTION_TEMPLATE.format(**db_info)
    
    db_manager = DBManager(connection_string, db_info.get('schema'))
    print(f"Connected to {db_info['database']}")
    
    model_class = db_manager.get_model_class(table_name)
    table = db_manager.get_table(table_name)
    
    print(f"Parsing: {data_file}")
    constraints = TableConstraints(table)
    parser = parser_class(constraints)
    parsed_entries = parser.parse(data_file)
    
    if (db_info.get('schema')):
        print(f"Updating rows for {db_info['schema']}.{table_name}")
    else:
        print(f"Updating rows for {table_name}")
    with db_manager as db:
        
        import time
        start = time.clock()
        
        num_merged = 0
        for entry in parsed_entries:
            db.merge(model_class(**entry))
            num_merged += 1
        db.commit()
        
        time_taken = time.clock() - start
        print(f"Merged {num_merged} records in {time_taken:0.2} seconds")

def main():
    
    parser = argparse.ArgumentParser(description='Loads data from an XLSX file.')
    # File options
    parser.add_argument('file', type=str,
                        help='the name of the file to parse')
    parser.add_argument('table', type=str,
                        help='the name of the table that the data belongs to')
    parser.add_argument('--xlsx', '-x', action='store_true',
                        help='use xlsx parser')
    # Database server options
    parser.add_argument('--host', '-H', type=str, default='localhost',
                        help='the host of the database server')
    parser.add_argument('--port', '-P', type=str, default='5432',
                        help='the port of the database server')
    # Database options
    parser.add_argument('--database', '-d', type=str,
                        help='the name of the database')
    parser.add_argument('--schema', '-s', type=str,
                        help='the database schema to use')
    parser.add_argument('--user', '-u', type=str,
                        help='the database user')
    parser.add_argument('--password', '-p', type=str,
                        help='the database user\'s password')
    
    args = parser.parse_args()
    
    db_user = args.user
    if not db_user:
        db_user = input("Database user:")
    
    db_password = args.password
    if not db_password:
        db_password = getpass()
    
    file_name = args.file
    table_name = args.table
    
    parser_class = CsvParser
    if args.xlsx:
        parser_class = XlsxParser
    
    db_info = {
        'host': args.host,
        'port': args.port,
        'database': args.database,
        'schema': args.schema,
        'user': db_user,
        'password': db_password,
    }
    
    load_model(file_name, table_name, db_info, parser_class)
