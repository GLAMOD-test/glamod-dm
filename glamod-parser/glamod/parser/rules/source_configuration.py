"""
Rules for source_configuration files.
"""

from dateutil.parser import parser as date_parser
from collections import OrderedDict as OD


class SourceConfigurationParserRules(object):
    
    fields = OD([
        ('source_id', (int,)),
        ('product_id', (None,)),
        ('product_name', (str,)),
        ('product_code', (str,)),
        ('product_version', (str,)),
        ('product_level', (str,)),
        ('product_uri', (str,)),
        ('description', (str,)),
        ('product_references', (str,)),
        ('product_citation', (str,)),
        ('product_status', (str,)),
        ('source_format', (int,)),
        ('source_format_version', (str,)),
        ('source_file', (str,)),
        ('source_file_checksum', (str,)),
        ('data_centre', (str,)),
        ('data_centre_url', (str,)),
        ('data_policy_licence', (str,)),
        ('contact', (str,)),
        ('contact_role', (str,)),
        ('history', (str,)),
        ('comments', (str,)),
        ('timestamp', (None,)),
        ('maintenance_and_update_frequency', (int,)),
        ('optional_data', (int,))
    ])

    code_table_lookups = {
        'source_format': 'SourceFormat' 
        } 
