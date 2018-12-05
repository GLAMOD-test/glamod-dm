"""
Rules for observations_table files.
"""

from glamod.parser.convertors import *
from glamod.parser.settings import *


from ._base import OD, _ParserRulesBase


class ObservationsTableParserRules(_ParserRulesBase):

    fields = OD([

      # Standard fields
        ('observation_id', str),
        ('report', str),
        ('data_policy_licence', int_or_empty),
        ('date_time', timestamp_or_empty),
        ('date_time_meaning', int_or_empty),
        ('observation_duration', int_or_empty),
        ('longitude', float_or_empty),
        ('latitude', float_or_empty),
#        ('crs', int_or_empty),
#        ('z_coordinate', float_or_empty),
#        ('z_coordinate_type', int_or_empty),
        ('observation_height_above_station_surface', float_or_empty),
        ('observed_variable', int_or_empty),
#        ('secondary_variable', int_or_empty),
        ('observation_value', float_or_empty),
        ('value_significance', int_or_empty),
        ('secondary_value', int),
        ('units', int_or_empty),
#        ('code_table', int_or_empty),
        ('conversion_flag', int_or_empty),
#        ('location_method', int_or_empty),
#        ('location_precision', float_or_empty),
#        ('z_coordinate_method', int_or_empty),
#        ('bbox_min_longitude', float_or_empty),
#        ('bbox_max_longitude', float_or_empty),
#        ('bbox_min_latitude', float_or_empty),
#        ('bbox_max_latitude', float_or_empty),
#        ('spatial_representativeness', int_or_empty),
        ('quality_flag', int_or_empty),
        ('numerical_precision', int),
#        ('sensor', int_or_empty),
#        ('sensor_automation_status', int_or_empty),
#        ('exposure_of_sensor', int_or_empty),
        ('original_precision', int),
        ('original_units', int_or_empty),
#        ('original_code_table', int_or_empty),
        ('original_value', float_or_empty),
        ('conversion_method', int_or_empty),
#        ('processing_code', str),
#        ('processing_level', int_or_empty),
#        ('adjustment', int_or_empty),
#        ('traceability', int_or_empty),
#        ('advanced_qc', int_or_empty),
#        ('advanced_uncertainty', int_or_empty),
#        ('advanced_homogenisation', int_or_empty),
        ('source', str),
    ])


    # Extended fields (not defined in table schema)
    #  - to be saved to the 'deliveries' DB for later lookups
    extended_fields = OD([
        ('region', (int,)),
        ('data_policy_licence', (int,)),
        ('primary_station_id_scheme', (int,)),
        ('location_accuracy', (float,)),
        ('location_method', (str,)),
        ('location_quality', (int,)),
        ('height_of_station_above_local_ground', (float_or_empty,)),
        ('height_of_station_above_sea_level', (float_or_empty,)),
        ('height_of_station_above_sea_level_accuracy', (float_or_empty,)),
        ('sea_level_datum', (float_or_empty,)),
        ('source_id', (str,))
    ])

    index_field = 'observation_id'

    code_table_fields = OD([

    ])

    # Structure of foreign key mappings:
    #   {<field_name>: (<app_model>, <field_to_write_to>, <is_primary_key>[BOOL])}
    # foreign_key_fields_to_add = OD([])
    # NOTE: This "foreign_key_fields_to_add" property is created in the base class
    #       as a reference to "code_table_fields". However, we might need them to be
    #       separate so the code treats them as separate.

