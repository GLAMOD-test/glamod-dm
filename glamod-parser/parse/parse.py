'''
Created on Nov 28, 2017

@author: William Tucker
'''

import argparse

from db.db_manager import DBManager
from db.table_constraints import TableConstraints

from parse.csv.csv_parser import CsvParser


CONNECTION_TEMPLATE = 'postgresql://{user}:{password}@{host}:{port}/{database}'


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
    # File options
    parser.add_argument('file', metavar='f', type=str,
                        help='the name of the file to parse')
    parser.add_argument('table', metavar='t', type=str,
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
        db_password = input("Database password:")
    
    connection_string = CONNECTION_TEMPLATE.format(user = db_user,
                                                   password = db_password,
                                                   host = args.host,
                                                   port = args.port,
                                                   database = args.database)
    
    db_manager = DBManager(connection_string, args.schema)
    
    file_name = args.file
    table_name = args.table
    
    load_model(file_name, table_name, db_manager)
