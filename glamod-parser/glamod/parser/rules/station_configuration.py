"""
Rules for station_configuration files.
""

class StationConfigurationParserRules(object):

    required_fields = ['col1']

    data_types = {
       'col1': str,
       'col2': int
    }

    defaults = {
       'col2': 0
    }
