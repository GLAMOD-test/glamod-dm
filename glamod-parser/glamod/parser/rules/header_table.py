"""
Rules for header_table files.
"""

from glamod.parser.convertors import *
from glamod.parser.settings import *


from ._base import OD, _ParserRulesBase


class HeaderTableParserRules(_ParserRulesBase):

    vlookup_fields = {
        'StationConfiguration': {
            'station_name': 'station_name',
            'station_type': 'station_type',
            'platform_type': 'platform_type',
            'platform_sub_type': 'platform_sub_type',
            'longitude': 'longitude',
            'latitude': 'latitude',
            'crs': 'station_crs'
        },
        'StationConfigurationLookupFields': {
            'region': 'region',
            'sub_region': 'operating_territory',
            'primary_station_id_scheme': 'primary_station_id_scheme',
            'location_accuracy': 'location_accuracy',
            'location_method': 'location_method',
            'location_quality': 'location_quality',
            'height_of_station_above_local_ground': 'height_of_station_above_local_ground',
            'height_of_station_above_sea_level': 'height_of_station_above_sea_level',
            'height_of_station_above_sea_level_accuracy': 'height_of_station_above_sea_level_accuracy',
            'sea_level_datum': 'sea_level_datum'
        }
    }

    fields = OD([
        ('report_id', str),
#        ('region', str),
#        ('sub_region', str),
        ('application_area', list_of_ints),
        ('observing_programme', list_of_ints),
        ('report_type', int_or_empty),
#        ('station_name', str),
#        ('station_type', str),
#        ('platform_type', str),
#        ('platform_sub_type', str),
        ('primary_station', str),
        ('station_record_number', int),
#        ('primary_station_id_scheme', str),
#        ('longitude', str),
#        ('latitude', str),
#        ('location_accuracy', str),
#        ('location_method', str),
#        ('location_quality', str),
#        ('crs', str),
        ('station_speed', float_or_empty),
        ('station_course', float_or_empty),
        ('station_heading', float_or_empty),
#        ('height_of_station_above_local_ground', str),
#        ('height_of_station_above_sea_level', str),
#        ('height_of_station_above_sea_level_accuracy', str),
#        ('sea_level_datum', str),
        ('report_meaning_of_time_stamp', int),
        ('report_timestamp', timestamp_or_empty),
        ('report_duration', int),
        ('report_time_accuracy', float_or_empty),
        ('report_time_quality', int),
        ('report_time_reference', int),
        ('profile', str),
        ('events_at_station', list_of_ints),
        ('report_quality', int),
        ('duplicate_status', int_or_empty),
        ('duplicates', list_of_strs),
        ('record_timestamp', timestamp_or_empty),
        ('history', str),
        ('processing_level', int_or_empty),
        ('processing_codes', list_of_ints),
        ('source', str),
        ('source_record_id', str)
    ])

    # Extended fields (not defined in table schema)
    #  - to be saved to the 'deliveries' DB for later lookups
    extended_fields = OD([
    ])

    index_field = 'report_id'

    code_table_fields = OD([
        ('report_type', (ReportIdType, 'type', True)),
        ('station_record_number', (StationConfiguration, 'record_number', True)),
        ('report_meaning_of_time_stamp', (MeaningOfTimeStamp, 'meaning', True)),
        ('report_time_quality', (TimeQuality, 'quality', True)),
        ('report_time_reference', (TimeReference, 'reference', True)),
        ('profile', (ProfileConfiguration, 'profile_id', True)),
        ('events_at_station', (EventsAtStation, 'event', True)),
        ('report_quality', (QualityFlag, 'flag', True)),
        ('duplicate_status', (DuplicateStatus, 'status', True)),
        ('processing_level', (ReportProcessingLevel, 'level', True)),
        ('processing_codes', (ReportProcessingCodes, 'code', True)),
        ('source', (SourceConfiguration, 'source_id', True)),
    ])



    # Structure of foreign key mappings:
    #   {<field_name>: (<app_model>, <field_to_write_to>, <is_primary_key>[BOOL])}
    # foreign_key_fields_to_add = OD([])
    # NOTE: This "foreign_key_fields_to_add" property is created in the base class
    #       as a reference to "code_table_fields". However, we might need them to be
    #       separate so the code treats them as separate.