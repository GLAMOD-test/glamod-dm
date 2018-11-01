"""
Rules for header_table files.
"""

from glamod.parser.convertors import *
from glamod.parser.settings import *


from glamod.parser.rules._base import OD, _ParserRulesBase


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
        ('report_id', (str,)),
#        ('region', (str,)),
#        ('sub_region', (str,)),
        ('application_area', (str,)),
        ('observing_programme', (str,)),
        ('report_type', (str,)),
#        ('station_name', (str,)),
#        ('station_type', (str,)),
#        ('platform_type', (str,)),
#        ('platform_sub_type', (str,)),
        ('primary_station', (str,)),
        ('station_record_number', (str,)),
#        ('primary_station_id_scheme', (str,)),
#        ('longitude', (str,)),
#        ('latitude', (str,)),
#        ('location_accuracy', (str,)),
#        ('location_method', (str,)),
#        ('location_quality', (str,)),
#        ('crs', (str,)),
        ('station_speed', (str,)),
        ('station_course', (str,)),
        ('station_heading', (str,)),
#        ('height_of_station_above_local_ground', (str,)),
#        ('height_of_station_above_sea_level', (str,)),
#        ('height_of_station_above_sea_level_accuracy', (str,)),
#        ('sea_level_datum', (str,)),
        ('report_meaning_of_time_stamp', (str,)),
        ('report_timestamp', (str,)),
        ('report_duration', (str,)),
        ('report_time_accuracy', (str,)),
        ('report_time_quality', (str,)),
        ('report_time_reference', (str,)),
        ('profile', (str,)),
        ('events_at_station', (str,)),
        ('report_quality', (str,)),
        ('duplicate_status', (str,)),
        ('duplicates', (str,)),
        ('record_timestamp', (str,)),
        ('history', (str,)),
        ('processing_level', (str,)),
        ('processing_codes', (str,)),
        ('source', (str,)),
        ('source_record_id', (str,))
    ])

    # Extended fields (not defined in table schema)
    #  - to be saved to the 'deliveries' DB for later lookups
    extended_fields = OD([
    ])

    index_field = 'primary_id'

    code_table_fields = OD([
        ('primary_id_scheme', IdScheme),
        ('secondary_id_scheme', IdScheme),
        ('station_crs', Crs),
        ('station_type', StationType),
        ('platform_type', PlatformType),
        ('platform_sub_type', PlatformSubType),
        ('operating_institute', Organisation),
        ('operating_territory', SubRegion),
        ('contact', Contact),
        ('role', Role),
        ('observing_frequency', ObservingFrequency),
        ('telecommunication_method', CommunicationMethod),
        ('station_automation', AutomationStatus),
        ('observed_variables', ObservedVariable),
        ('optional_data', DataPresent),
        ('region', Region)
    ])

    # Structure of foreign key mappings:
    #   {<field_name>: (<app_model>, <field_to_write_to>, <is_primary_key>[BOOL])}
    foreign_key_fields_to_add = OD([
        ('primary_id_scheme', (IdScheme, 'scheme', True)),
        ('secondary_id_scheme', (IdScheme, 'scheme', True)),
        ('station_crs', (Crs, 'crs', True)),
        ('station_type', (StationType, 'type', True)),
        ('platform_type', (PlatformType, 'type', True)),
        ('platform_sub_type', (PlatformSubType, 'sub_type', True)),
        ('operating_institute', (Organisation, 'organisation_id', True)),
        ('operating_territory', (SubRegion, 'sub_region', True)),
        ('contact', (Contact, 'contact_id', True)),
        ('role', (Role, 'role', True)),
        ('observing_frequency', (ObservingFrequency, 'frequency', True)),
        ('telecommunication_method', (CommunicationMethod, 'method', True)),
        ('station_automation', (AutomationStatus, 'automation', True)),
        ('observed_variables', (ObservedVariable, 'variable', True)),
        ('optional_data', (DataPresent, 'flag', True))
    ])


