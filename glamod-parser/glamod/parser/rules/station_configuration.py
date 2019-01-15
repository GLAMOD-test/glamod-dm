"""
Rules for station_configuration files.
"""

from glamod.parser.convertors import *
from glamod.parser.settings import *


from ._base import OD, _ParserRulesBase


class StationConfigurationParserRules(_ParserRulesBase):

    fields = OD([

      # Standard fields
        ('primary_id', str),
        ('primary_id_scheme', int_or_empty),
        ('record_number', int),
        ('secondary_id', list_of_strs),
        ('secondary_id_scheme', list_of_ints),
        ('station_name', str),
        ('station_abbreviation', str),
        ('alternative_name', list_of_strs),
        ('station_crs', str),
        ('longitude', float),
        ('latitude', float),
        ('local_gravity', float_or_empty),
        ('start_date', timestamp_or_empty),
        ('end_date', timestamp_or_empty),
        ('station_type', int_or_empty),
        ('platform_type', int_or_empty),
        ('platform_sub_type', int_or_empty),
        ('operating_institute', str),
        ('operating_territory', int_or_empty),
        ('city', str),
        ('contact', list_of_strs),
        ('role', list_of_ints),
        ('observing_frequency', int_or_empty),
        ('reporting_time', list_of_ints),
        ('telecommunication_method', list_of_ints),
        ('station_automation', int_or_empty),
        ('measuring_system_model', list_of_strs),
        ('measuring_system_id', list_of_strs),
        ('observed_variables', list_of_ints),
        ('comment', str),
        ('optional_data', int_or_empty),
        ('bbox_min_longitude', float_or_empty),
        ('bbox_max_longitude', float_or_empty),
        ('bbox_min_latitude', float_or_empty),
        ('bbox_max_latitude', float_or_empty),
        ('metadata_contact', list_of_strs),
        ('metadata_contact_role', list_of_ints),
    ])


    # Extended fields (not defined in table schema)
    #  - to be saved to the 'deliveries' DB for later lookups
    extended_fields = OD([
        ('region', int_or_empty),
        ('data_policy_licence', int_or_empty),
        ('primary_station_id_scheme', int_or_empty),
        ('location_accuracy', float),
        ('location_method', int_or_empty),
        ('location_quality', int_or_empty),
        ('height_of_station_above_local_ground', float_or_empty),
        ('height_of_station_above_sea_level', float_or_empty),
        ('height_of_station_above_sea_level_accuracy', float_or_empty),
        ('sea_level_datum', float_or_empty),
        ('source_id', str)
    ])

    extended_fields_to_duplicate = ('primary_id', 'record_number')

    index_field = 'primary_id'

    code_table_fields = OD([
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
            ('region', (Region, 'region', True)),
            ('data_policy_licence', (DataPolicyLicence, 'policy', True)),
            ('optional_data', (DataPresent, 'flag', True)),
            ('location_method', (LocationMethod, 'method', True)),
            ('location_quality', (LocationQuality, 'quality', True)),
            ('sea_level_datum', (SeaLevelDatum, 'datum', True))
    ])


    # Structure of foreign key mappings:
    #   {<field_name>: (<app_model>, <field_to_write_to>, <is_primary_key>[BOOL])}
    # foreign_key_fields_to_add = OD([])
    # NOTE: This "foreign_key_fields_to_add" property is created in the base class
    #       as a reference to "code_table_fields". However, we might need them to be
    #       separate so the code treats them as separate.