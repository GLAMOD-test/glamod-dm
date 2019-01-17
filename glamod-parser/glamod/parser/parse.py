'''
Created on 28/09/2018

@author: Ag Stephens
'''

import os
import click
import logging

from glamod.parser.utils import timeit, unzip
from glamod.parser.processors import (SourceAndStationConfigProcessor,
                                      HeaderAndObsTableProcessor)


logger = logging.getLogger(__package__)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")


@click.command()
@click.option('-t', '--del-type', type=click.Choice(['source', 'data']),
              help='Specify file types to process ("source" or "data").')
@click.option('-d', '--working_dir', default='working_dir', 
              help='Working directory to unzip files to.')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Verbose output.')
@click.argument('location', type=click.Path(exists=True)) 
def parse_delivery(location, del_type, verbose, working_dir='working_dir'):

    log_level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(log_level)

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
    logger.info('Beginning parsing of SOURCE and STATION files at: '
          '{}'.format(location))

    processor = SourceAndStationConfigProcessor(location)
    processor.run()
    

@timeit
def parse_data_delivery(location):
    logger.info('INFO', 'Beginning parsing of HEADER and OBSERVATIONS TABLE '
          'files at: {}'.format(location))

    processor = HeaderAndObsTableProcessor(location)
    processor.run()



if __name__ == '__main__':

    parse_delivery()

