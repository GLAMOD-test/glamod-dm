"""
Rules for observations_table files.
"""

from glamod.parser.convertors import int_or_empty, float_or_empty, \
    timestamp_or_empty
from cdmapp.models import MeaningOfTimestamp, Duration, ObservedVariable, \
    ObservationValueSignificance, HeaderTable, DataPolicyLicence, Units, \
    ConversionFlag, SourceConfiguration, QualityFlag, ConversionMethod

from ._base import OD, _ParserRulesBase, ForeignKeyLookup


class ObservationsTableParserRules(_ParserRulesBase):

    lookups = [
        ForeignKeyLookup('report_id', HeaderTable, 'report_id',
            extra_fields = {
                'report_type': 'report_type',
                'station_type': 'station_type',
            }
        ),
        ForeignKeyLookup('report_id', HeaderTable, 'report_id'),
        ForeignKeyLookup('data_policy_licence', DataPolicyLicence, 'policy'),
        ForeignKeyLookup('date_time_meaning', MeaningOfTimestamp, 'meaning'),
        ForeignKeyLookup('observation_duration', Duration, 'duration'),
        ForeignKeyLookup('value_significance', ObservationValueSignificance, 'significance'),
        ForeignKeyLookup('units', Units, 'units'),
        ForeignKeyLookup('conversion_flag', ConversionFlag, 'flag'),
        ForeignKeyLookup('quality_flag', QualityFlag, 'flag'),
        ForeignKeyLookup('original_units', Units, 'units'),
        ForeignKeyLookup('conversion_method', ConversionMethod, 'method',
            query_map = { 'observed_variable': 'variable' }
        ),
        ForeignKeyLookup('observed_variable', ObservedVariable, 'variable'),
        ForeignKeyLookup('source_id', SourceConfiguration, 'source_id'),
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
        ('observation_height_above_station_surface', float_or_empty),
        ('observed_variable', int_or_empty),
        ('observation_value', float_or_empty),
        ('value_significance', int_or_empty),
        ('secondary_value', int_or_empty),
        ('units', int_or_empty),
        ('conversion_flag', int_or_empty),
        ('quality_flag', int_or_empty),
        ('numerical_precision', float_or_empty),
        ('original_precision', float_or_empty),
        ('original_units', int_or_empty),
        ('original_value', float_or_empty),
        ('conversion_method', int_or_empty),
        ('source_id', str),
    ])


    index_field = 'observation_id'

    code_table_fields = OD([
    ])
