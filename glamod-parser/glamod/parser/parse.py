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


