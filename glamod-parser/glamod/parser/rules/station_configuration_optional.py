"""
Rules for station_configuration files.
"""

from glamod.parser.convertors import str_strip, int_or_empty
from cdmapp.models import StationConfiguration, \
    StationConfigurationFields, Kind

from ._base import OD, _ParserRulesBase, ForeignKeyLookup


class StationConfigurationOptionalParserRules(_ParserRulesBase):
    
    lookups = [
        ForeignKeyLookup('station_primary_id', StationConfiguration, 'primary_id'),
        ForeignKeyLookup('kind', Kind, 'kind'),
        ForeignKeyLookup('field', StationConfigurationFields, 'field_id'),
    ]
    
    fields = OD([
        ('station_primary_id', str_strip),
        ('record_number', int),
        ('kind', int_or_empty),
        ('field', str),
        ('value', str),
        ('comments', str),
    ])

    index_field = 'station_primary_id'
