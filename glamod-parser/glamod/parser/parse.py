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


def load_model(data_file, table_name, db_info, merge=False,
               null_values=None, use_default_null=True,
               ignore_columns=None, parser_class=CsvParser):
    
    connection_string = CONNECTION_TEMPLATE.format(**db_info)
    
    db_manager = DBManager(connection_string, db_info.get('schema'))
    print(f"Connected to {db_info['database']}")
    
    model_class = db_manager.get_model_class(table_name)
    table = db_manager.get_table(table_name)
    constraints = TableConstraints(table)
    
    parser = parser_class(constraints,
                          null_values=null_values,
                          use_default_null=use_default_null)
    
    print(f"Parsing: {data_file}")
    if ignore_columns:
        print(f"Ignore columns: {' '.join(ignore_columns)}")
    parsed_entries = parser.parse(data_file,
                                  ignore_columns=ignore_columns)
    
    if (db_info.get('schema')):
        print(f"Updating rows for {db_info['schema']}.{table_name}")
    else:
        print(f"Updating rows for {table_name}")
    with db_manager as db:
        
        import time
        start = time.clock()
        
        row_count = 0
        if merge:
            
            for entry in parsed_entries:
                db.merge(model_class(**entry))
                row_count += 1
            
        else:
            
            model_instances = []
            for entry in parsed_entries:
                model_instances.append(model_class(**entry))
            row_count = len(model_instances)
            
            db.bulk_save(model_instances)
        
        db.commit()
        
        seconds = time.clock() - start
        minutes, seconds = divmod(seconds, 60)
        
        if minutes > 0:
            time_taken = f"{int(minutes)} minutes and {int(seconds)} seconds"
        else:
            time_taken = f"{seconds:.2f} seconds"
        
        print(f"Merged {row_count} records in {time_taken}")

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
    # Extra options
    parser.add_argument('--merge', '-m', action='store_true',
                        help='merge rows if primary key already exists')
    parser.add_argument('--null-values', '-n', type=str, action='append',
                        help='values which should equal NULL in the database')
    parser.add_argument('--no-parse-null', '-N', action='store_false',
                        help='switch off default NULL value parsing')
    parser.add_argument('--ignore', '-i', type=str, action='append',
                        help='columns to ignore')
    
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
    
    load_model(file_name, table_name, db_info, merge=args.merge,
               null_values=args.null_values, use_default_null=args.no_parse_null,
               ignore_columns=args.ignore, parser_class=parser_class)
