"""
Rules for source_configuration files.
"""

from glamod.parser.convertors import *
from glamod.parser.settings import *

from ._base import OD, _ParserRulesBase


class SourceConfigurationParserRules(_ParserRulesBase):
    
    fields = OD([
        ('source_id', (int,)),
        ('product_id', (None,)),
        ('product_name', (str,)),
        ('product_code', (str,)),
        ('product_version', (str,)),
        ('product_level', (int_or_empty,)),
        ('product_uri', (str,)),
        ('description', (str,)),
        ('product_references', (str,)),
        ('product_citation', (str,)),
        ('product_status', (str,)),
        ('source_format', (int_or_empty,)),
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
        ('timestamp', (timestamp_or_empty,)),
        ('maintenance_and_update_frequency', (int_or_empty,)),
        ('optional_data', (int_or_empty,))
    ])

    index_field = 'source_id'

    code_table_fields = OD([
        ('product_level', ProductLevel), 
        ('product_status', ProductStatus),
        ('source_format', SourceFormat),
        ('data_centre', Organisation),
        ('data_policy_licence', DataPolicyLicence),
        ('contact', Contact),
        ('contact_role', Role),
        ('maintenance_and_update_frequency', UpdateFrequency),
        ('optional_data', DataPresent)
    ])

    # Structure of foreign key mappings:
    #   {<field_name>: (<app_model>, <field_to_write_to>, <is_primary_key>[BOOL])}
    foreign_key_fields_to_add = OD([
        ('product_level', (ProductLevel, 'description', False)),
        ('product_status', (ProductStatus, 'description', False)),
        ('contact', (Contact, 'contact_id', True)),
        ('data_centre', (Organisation, 'organisation_id', True)),
        ('data_policy_licence', (DataPolicyLicence, 'description', False))
    ])
