'''
Created on 28/09/2018

@author: Ag Stephens
'''

import os

import click

from glamod.parser.utils import timeit, unzip, log
from glamod.parser.processors import (SourceAndStationConfigProcessor,
                                      HeaderAndObsTableProcessor)


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


@timeit
def parse_source_station_delivery(location):
    log('INFO', 'Beginning parsing of SOURCE and STATION files at: '
          '{}'.format(location))

    processor = SourceAndStationConfigProcessor(location)
    processor.run()
    

@timeit
def parse_data_delivery(location):
    log('INFO', 'Beginning parsing of HEADER and OBSERVATIONS TABLE '
          'files at: {}'.format(location))

    processor = HeaderAndObsTableProcessor(location)
    processor.run()



if __name__ == '__main__':

    parse_delivery()

