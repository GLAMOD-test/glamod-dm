"""
Rules for header_table files.
"""

from glamod.parser.convertors import *
from glamod.parser.settings import *


from ._base import OD, _ParserRulesBase, ForeignKeyLookup, LinkedLookup


class HeaderTableParserRules(_ParserRulesBase):

    vlookups = [
        ForeignKeyLookup('primary_station_id', StationConfiguration, 'primary_id',
            extra_fields = {
                'station_name': 'station_name',
                'station_type': 'station_type',
                'platform_type': 'platform_type',
                'platform_sub_type': 'platform_sub_type',
                'longitude': 'longitude',
                'latitude': 'latitude',
                'sub_region': 'operating_territory',
                'crs': 'station_crs'
            }
        ),
        LinkedLookup('primary_station_id', StationConfigurationLookupFields,
            {'primary_id': 'primary_id', 'record_number': 'record_number'},
            extra_fields = {
                'region': 'region',
                'primary_station_id_scheme': 'primary_station_id_scheme',
                'location_accuracy': 'location_accuracy',
                'location_method': 'location_method',
                'location_quality': 'location_quality',
                'height_of_station_above_local_ground': 'height_of_station_above_local_ground',
                'height_of_station_above_sea_level': 'height_of_station_above_sea_level',
                'height_of_station_above_sea_level_accuracy': 'height_of_station_above_sea_level_accuracy',
                'sea_level_datum': 'sea_level_datum'
            }
        ),
        ForeignKeyLookup('region', Region, 'region'),
        ForeignKeyLookup('primary_station_id_scheme', IdScheme, 'scheme'),
        ForeignKeyLookup('location_method', LocationMethod, 'method'),
        ForeignKeyLookup('location_quality', LocationQuality, 'quality'),
        ForeignKeyLookup('sea_level_datum', SeaLevelDatum, 'datum'),
    ]

    fields = OD([
        ('report_id', str),
        ('application_area', list_of_ints),
        ('observing_programme', list_of_ints),
        ('report_type', int_or_empty),
        ('primary_station_id', str),
        ('station_record_number', int_or_empty),
        ('report_meaning_of_timestamp', int_or_empty),
        ('report_timestamp', timestamp_or_empty),
        ('report_duration', int_or_empty),
        ('report_time_accuracy', float_or_empty),
        ('report_time_quality', int_or_empty),
        ('report_time_reference', int_or_empty),
        ('profile_id', str),
        ('events_at_station', list_of_ints),
        ('report_quality', int_or_empty),
        ('duplicate_status', int_or_empty),
        ('duplicates', list_of_strs),
        ('record_timestamp', timestamp_or_empty),
        ('history', str),
        ('processing_level', int_or_empty),
        ('processing_codes', list_of_ints),
        ('source_id', str),
    ])

    # Empty fields: excluded fields that should be added in by the parser
    # as empty values.
    empty_fields = OD([

    ])

    # Extended fields (not defined in table schema)
    #  - to be saved to the 'deliveries' DB for later lookups
    extended_fields = OD([
    ])

    index_field = 'report_id'

    code_table_fields = OD([
        ('report_type', (ReportType, 'type', True)),
        ('report_meaning_of_timestamp', (MeaningOfTimestamp, 'meaning', True)),
        ('report_duration', (Duration, 'duration', True)),
        ('report_time_quality', (TimeQuality, 'quality', True)),
        ('report_time_reference', (TimeReference, 'reference', True)),
        ('profile_id', (ProfileConfiguration, 'profile_id', True)),
        ('events_at_station', (EventsAtStation, 'event', True)),
        ('report_quality', (QualityFlag, 'flag', True)),
        ('duplicate_status', (DuplicateStatus, 'status', True)),
        ('processing_level', (ReportProcessingLevel, 'level', True)),
        ('processing_codes', (ReportProcessingCodes, 'code', True)),
        ('source_id', (SourceConfiguration, 'source_id', True)),
    ])



    # Structure of foreign key mappings:
    #   {<field_name>: (<app_model>, <field_to_write_to>, <is_primary_key>[BOOL])}
    # foreign_key_fields_to_add = OD([])
    # NOTE: This "foreign_key_fields_to_add" property is created in the base class
    #       as a reference to "code_table_fields". However, we might need them to be
    #       separate so the code treats them as separate.