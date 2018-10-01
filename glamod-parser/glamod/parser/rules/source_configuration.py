"""
Rules for source_configuration files.
""

class SourceConfigurationParserRules(object):

    required_fields = ['source_id', 'product_id', 'product_name', 'product_code', 
                       'product_version', 'product_level', 'product_uri', 
                       'description', 'product_references', 'product_citation', 
                       'product_status', 'source_format', 'source_format_version', 
                       'source_file', 'source_file_checksum', 'data_centre', 
                       'data_centre_url', 'data_policy_licence', 'contact', 
                       'contact_role', 'history', 'comments', 'timestamp', 
                       'maintenance_and_update_frequency', 'optional_data']


    data_types = {
       'col1': str,
       'col2': int
    }

    defaults = {
       'col2': 0
    }



