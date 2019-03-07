'''
Created on 28/09/2018

@author: Ag Stephens
'''

import os
import click
import logging
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'glamod_site.settings'
django.setup()

from glamod.parser.utils import timeit, unzip
from glamod.parser.processors import (SourceConfigurationProcessor,
    StationConfigurationProcessor, StationConfigurationOptionalProcessor,
    HeaderTableProcessor, ObservationsTableProcessor)


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
@click.option('-w', '--write', is_flag=True, default=False,
              help='Write to the database.')
@click.option('-b', '--bulk', is_flag=True, default=False,
              help='Bulk Write to the database.')
@click.argument('location', type=click.Path(exists=True)) 
def parse_delivery(location, del_type, verbose, write, bulk, working_dir='working_dir'):

    log_level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(log_level)

    if os.path.isfile(location):
        if not os.path.splitext(location)[-1] == '.zip':
            raise ValueError('If "location" is a file it must end in ".zip".')

        location = unzip(location, target_dir=working_dir)

    if del_type == 'source':
        parse_source_station_delivery(
            location, write_to_db=write, bulk_write=bulk)
    elif del_type == 'data':
        parse_data_delivery(
            location, write_to_db=write, bulk_write=bulk)
    else:
        raise ValueError('Unknown delivery type: {}'.format(del_type))


@timeit
def parse_source_station_delivery(
        location, write_to_db=False, bulk_write=False):
    logger.info('Beginning parsing of SOURCE and STATION files at: '
          '{}'.format(location))
    
    processor_classes = [
        SourceConfigurationProcessor,
        StationConfigurationProcessor,
        StationConfigurationOptionalProcessor,
    ]
    
    for processor_class in processor_classes:
        processor = processor_class(location)
        processor.run()
        
        if write_to_db:
            processor.write_to_db(bulk=bulk_write)

@timeit
def parse_data_delivery(
        location, write_to_db=False, bulk_write=False):
    logger.info('Beginning parsing of HEADER and OBSERVATIONS TABLE '
          'files at: {}'.format(location))
    
    processor_classes = [
        HeaderTableProcessor,
        ObservationsTableProcessor,
    ]
    
    for processor_class in processor_classes:
        processor = processor_class(location)
        processor.run()
        
        if write_to_db:
            processor.write_to_db(bulk=bulk_write)


if __name__ == '__main__':

    parse_delivery()
