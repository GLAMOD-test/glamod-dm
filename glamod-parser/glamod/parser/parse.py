'''
Created on 28/09/2018

@author: Ag Stephens
'''

import os

import click

from glamod.parser.utils import timeit, unzip

from glamod.parser.structure_check import *
from glamod.parser.csv_parser.csv_parser import CsvParser



@click.command()
@click.option('--stations-only', is_flag=True, default=False, 
              help='Only parse "SOURCE" and "STATION" configuration files.')
@click.option('--working_dir', default='working_dir', 
              help='Working directory to unzip files to.')
@click.argument('location', type=click.Path(exists=True)) 
def parse_delivery(location, stations_only=False, working_dir='working_dir'):

    if os.path.isfile(location):
        if not os.path.splitext(location)[-1] == '.zip':
            raise ValueError('If "location" is a file it must end in ".zip".')

        location = unzip(location, target_dir=working_dir)

    if stations_only:
        parse_source_and_station_configs(location)
    else:
        parse_complete_delivery(location)

    
@timeit
def parse_source_and_station_configs(location):
    print('[INFO] Beginning parsing of SOURCE and STATION files at: '
          '{}'.format(location))
    SourceAndStationConfigStructureCheck(location)
 

@timeit
def parse_complete_delivery(location):
    print('[INFO] Beginning parsing of HEADER and OBSERVATIONS TABLE '
          'files at:  {}'.format(location))
    CompleteStructureCheck(location)


def OLDmain():
    

    parser = argparse.ArgumentParser(description='Parses and manages a GLAMOD data delivery')
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
