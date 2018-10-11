'''
Created on 28/09/2018

@author: Ag Stephens
'''

import os

import click

from glamod.parser.utils import timeit, unzip, log, get_content_check

from glamod.parser.structure_check import *


@click.command()
@click.option('-t', '--del-type', type=click.Choice(['source', 'data']),
              help='Only parse "SOURCE" and "STATION" configuration files.')
@click.option('-d', '--working_dir', default='working_dir', 
              help='Working directory to unzip files to.')
@click.argument('location', type=click.Path(exists=True)) 
def parse_delivery(location, del_type, working_dir='working_dir'):

    if os.path.isfile(location):
        if not os.path.splitext(location)[-1] == '.zip':
            raise ValueError('If "location" is a file it must end in ".zip".')

        location = unzip(location, target_dir=working_dir)

    if del_type == 'source':
        parse_source_station_delivery(location)
    elif del_type == 'data':
        parse_data_delivery(location)
    else:
        raise ValueError('Unknown delivery type: {}'.format(del_type))


def _run_content_checks(fpaths):
    
    for fpath in fpaths:
        content_check = get_content_check(fpath)
        content_check.run()

    
@timeit
def parse_source_station_delivery(location):
    log('INFO', 'Beginning parsing of SOURCE and STATION files at: '
          '{}'.format(location))

    structure_check = SourceAndStationConfigStructureCheck(location)
    structure_check.run()
    _run_content_checks(structure_check.get_files())
    
     
    

@timeit
def parse_data_delivery(location):
    log('INFO', 'Beginning parsing of HEADER and OBSERVATIONS TABLE '
          'files at:  {}'.format(location))

    structure_checks = [HeaderStructureCheck, ObservationsStructureCheck]
 
    for structure_check in structure_checks:
        check = structure_check(location)
        check.run()
    
    _run_content_checks(structure_check.get_files())





