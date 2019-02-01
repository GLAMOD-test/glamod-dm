"""
Rules for observations_table files.
"""

from glamod.parser.convertors import *
from glamod.parser.settings import *


from ._base import OD, _ParserRulesBase, ForeignKeyLookup
from cdmapp.models import MeaningOfTimestamp, Duration, ObservedVariable,\
    ObservationValueSignificance, SecondaryVariable, ZCoordinateType, Units,\
    ObservationCodeTable, ConversionFlag, LocationMethod, ZCoordinateMethod,\
    SpatialRepresentativeness, QualityFlag, SensorConfiguration,\
    AutomationStatus, InstrumentExposureQuality, ConversionMethod,\
    ProcessingCode, ProcessingLevel, Adjustment, Traceability, DataPresent


class ObservationsTableParserRules(_ParserRulesBase):

    vlookups = [
        ForeignKeyLookup('report_id', HeaderTable, 'report_id',
            extra_fields = {
                'report_type': 'report_type',
                'station_type': 'station_type',
            }
        ),
    ]

    fields = OD([

      # Standard fields
        ('observation_id', str),
        ('report_id', str),
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
        ('secondary_value', int_or_empty),
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
        ('numerical_precision', float_or_empty),
#        ('sensor', int_or_empty),
#        ('sensor_automation_status', int_or_empty),
#        ('exposure_of_sensor', int_or_empty),
        ('original_precision', float_or_empty),
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
        ('source_id', str),
    ])


    index_field = 'observation_id'

    code_table_fields = OD([
        ('report_id', (HeaderTable, 'report_id', True)),
        ('data_policy_licence', (DataPolicyLicence, 'policy', True)),
        ('date_time_meaning', (MeaningOfTimestamp, 'meaning', True)),
        ('observation_duration', (Duration, 'duration', True)),
#        ('crs', (CRS, 'crs', True)),
#        ('z_coordinate_type', (ZCoordinateType, 'type', True)),
        ('observed_variable', (ObservedVariable, 'variable', True)),
#        ('secondary_variable', (SecondaryVariable, 'variable', True)),
        ('value_significance', (ObservationValueSignificance, 'significance', True)),
#        ('secondary_value', (SecondaryVariable, 'value', True)),
        ('units', (Units, 'units', True)),
#        ('code_table', (ObservationCodeTable, 'code_table', True)),
        ('conversion_flag', (ConversionFlag, 'flag', True)),
#        ('location_method', (LocationMethod, 'method', True)),
#        ('z_coordinate_method', (ZCoordinateMethod, 'method', True)),
#        ('spatial_representativeness', (SpatialRepresentativeness, 'representativeness', True)),
        ('quality_flag', (QualityFlag, 'flag', True)),
#        ('sensor_id', (SensorConfiguration, 'sensor_id', True)),
#        ('sensor_automation_status', (AutomationStatus, 'automation', True)),
#        ('exposure_of_sensor', (InstrumentExposureQuality, 'exposure', True)),
        ('original_units', (Units, 'units', True)),
#        ('original_code_table', (ObservationCodeTable, 'code_table', True)),
        ('conversion_method', (ConversionMethod, 'method', True)),
#        ('processing_code', (ProcessingCode, 'code', True)),
#        ('processing_level', (ProcessingLevel, 'level', True)),
#        ('adjustment_id', (Adjustment, 'adjustment_id', True)),
#        ('traceability', (Traceability, 'traceability', True)),
#        ('advanced_qc', (DataPresent, 'flag', True)),
#        ('advanced_uncertainty', (DataPresent, 'flag', True)),
#        ('advanced_homogenisation', (DataPresent, 'flag', True)),
        ('source_id', (SourceConfiguration, 'source_id', True)),
    ])

    # Structure of foreign key mappings:
    #   {<field_name>: (<app_model>, <field_to_write_to>, <is_primary_key>[BOOL])}
    # foreign_key_fields_to_add = OD([])
    # NOTE: This "foreign_key_fields_to_add" property is created in the base class
    #       as a reference to "code_table_fields". However, we might need them to be
    #       separate so the code treats them as separate.

