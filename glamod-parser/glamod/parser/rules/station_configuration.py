"""
Rules for station_configuration files.
"""

from collections import OrderedDict as OD


class StationConfigurationParserRules(object):

    fields = OD([
        ('primary_id', (str,)),
        ('primary_id_scheme', (str,)),
        ('record_number', (str,)),
        ('secondary_id', (str,)),
        ('secondary_id_scheme', (str,)),
        ('station_name', (str,)),
        ('station_abbreviation', (str,)),
        ('alternative_name', (str,)),
        ('station_crs', (str,)),
        ('longitude', (str,)),
        ('latitude', (str,)),
        ('local_gravity', (str,)),
        ('start_date', (str,)),
        ('end_date', (str,)),
        ('station_type', (str,)),
        ('platform_type', (str,)),
        ('platform_sub_type', (str,)),
        ('operating_institute', (str,)),
        ('operating_territory', (str,)),
        ('city', (str,)),
        ('contact', (str,)),
        ('role', (str,)),
        ('observing_frequency', (str,)),
        ('reporting_time', (str,)),
        ('telecommunication_method', (str,)),
        ('station_automation', (str,)),
        ('measuring_system_model', (str,)),
        ('measuring_system_id', (str,)),
        ('observed_variables', (str,)),
        ('comment', (str,)),
        ('optional_data', (str,)),
        ('region', (str,)),
        ('sub_region', (str,)),
        ('data_policy_licence', (str,)),
        ('station_record_number', (str,)),
        ('primary_station_id_scheme', (str,)),
        ('location_accuracy', (str,)),
        ('location_method', (str,)),
        ('location_quality', (str,)),
        ('height_of_station_above_local_ground', (str,)),
        ('height_of_station_above_sea_level', (str,)),
        ('height_of_station_above_sea_level_accuracy', (str,)),
        ('sea_level_datum', (str,)),
        ('source_id', (str,))
    ])

