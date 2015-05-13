import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.plugins.toolkit import Invalid

def frequency_validator(value, context):
    if value not in ['daily', 'weekly', 'monthly', 'biannually', 'annually', 'infrequently', 'never']:
        raise Invalid("Invalid frequency")
    return value

def get_frequency_translation(frequency):
    freqmap = {
        'daily': 'Daily',
        'weekly': 'Weekly',
        'monthly': 'Monthly',
        'biannually': 'Biannually',
        'annually': 'Annually',
        'infrequently': 'Infrequently',
        'never': 'Never'
    }
    return freqmap[frequency]

class CphmetadataPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IRoutes, inherit=True)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'cphmetadata')

    def create_package_schema(self):
        # let's grab the default schema in our plugin
        schema = super(CphmetadataPlugin, self).create_package_schema()
        schema.update({
            'custom_text': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'update_frequency': [frequency_validator,
                            toolkit.get_converter('convert_to_extras')]
        })
        return schema

    def update_package_schema(self):
        schema = super(CphmetadataPlugin, self).update_package_schema()
        #our custom field
        schema.update({
            'custom_text': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'update_frequency': [frequency_validator,
                            toolkit.get_converter('convert_to_extras')]
        })
        return schema

    def show_package_schema(self):
        schema = super(CphmetadataPlugin, self).show_package_schema()
        schema.update({
            'custom_text': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')],
            'update_frequency': [frequency_validator,
                            toolkit.get_converter('convert_from_extras')]
        })
        return schema

    def is_fallback(self):
        return True

    def package_types(self):
        #return ["dataset"]
        return []

    def get_helpers(self):
        return {'get_frequency_translation': get_frequency_translation}
    
    def before_map(self, map):
        ''' IRoutes '''
        #Override new dataset so we can optionally skip resource adding
        pkg_ctrl = 'ckanext.cphmetadata.controllers.package:MetadataPackageController'
        map.connect('add dataset', '/dataset/new', controller=pkg_ctrl, action='new')
        return map
