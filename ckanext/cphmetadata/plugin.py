#!/usr/bin/python
# -*- coding: utf-8 -*-
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h
from ckan.plugins.toolkit import Invalid
import datetime
import uuid
from ckan.logic import get_action

def frequency_validator(value, context):
    if value not in ['daily', 'weekly', 'monthly','quarterly', 'biannually', 'annually','regularly', 'infrequently', 'never', '']:
        raise Invalid("Invalid frequency")
    return value

def quality_validator(value, context):
    if value not in ['good', 'medium', 'bad']:
        raise Invalid("Invalid quality")
    return value

def get_quality_translation(quality):
    qualmap = {
        'good': 'Total ajourført',
        'medium': 'Delvist ajourført',
        'bad': 'Mangelfuldt'
    }
    return qualmap.get(quality, '').decode('utf8')


def get_frequency_translation(frequency):
    #It was decided after import that the default should be '', therefore created
    #another value for never and mapped current never to an empty string.
    #Nicolai: Changed translations to danish as with quality
    freqmap = {
        'daily': 'Dagligt',
        'weekly': 'Ugentligt',
        'monthly': 'Månedligt',
	'quarterly': 'Kvartalsvist',
        'biannually': 'Halvårligt',
        'annually': 'Årligt',
        'infrequently': 'Sjældent',
	'regularly': 'Jævnligt',
        'never': 'Aldrig',
    }
    return freqmap.get(frequency, '').decode('utf8')

class CphmetadataPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IPackageController, inherit=True)  
   
    ## IPackageController
    def after_create(self, context, pkg_dict):
        """ Dataset is updated (Or created finally - after draft)
            Assign a UUID to the dataset if possible
        """
	# Stupid hack because model is not comitted until after timestamps
	# And we cant timestamp before model is created (BAD)
	# Commit the model to the repo so we dont get internal server error
	# Fix found on Github/ckan

	if 'model' in context:
	    context['model'].repo.commit()

	#Generate a uuid4
        metadataID = str(uuid.uuid4())
        update_data = get_action('package_show')(context, {'id': pkg_dict['id']})

        if(update_data['metadata_id'] == "" and metadataID != ""):
            update_data['metadata_id'] = metadataID
            get_action('package_update')(context,update_data)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'cphmetadata')

    def create_package_schema(self):
        # let's grab the default schema in our plugin
	# Department -> Center
	# Office -> Enhed
	
        schema = super(CphmetadataPlugin, self).create_package_schema()
        schema.update({
            'update_frequency': [frequency_validator,
                            toolkit.get_converter('convert_to_extras')],
	    'update_frequency_note': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'department': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'office': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
	    'office_email': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'editor': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'kkkort': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'copenhagenkortet': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'datakk': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'date_created': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'date_updated': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'data_quality': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'quality_note': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
	    'bydata': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'bydata_email': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'metadata_id': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
        })
        return schema

    def update_package_schema(self):
        schema = super(CphmetadataPlugin, self).update_package_schema()
        #our custom fields
        schema.update({
            'update_frequency': [frequency_validator,
                            toolkit.get_converter('convert_to_extras')],
	    'update_frequency_note': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'department': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'office': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'office_email': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'editor': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'kkkort': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'copenhagenkortet': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'datakk': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'date_created': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'date_updated': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'data_quality': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'quality_note': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'bydata': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'bydata_email': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'metadata_id': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
        })
        return schema

    def show_package_schema(self):
        schema = super(CphmetadataPlugin, self).show_package_schema()
        schema.update({
            'custom_text': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')],
            'update_frequency': [frequency_validator,
                            toolkit.get_converter('convert_from_extras')],
 	    'update_frequency_note': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')],
            'department': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')],
            'office': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')],
	    'office_email': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')],
            'editor': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')],
            'kkkort': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')],
            'copenhagenkortet': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')],
            'datakk': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')],
            'date_created': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')],
            'date_updated': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')],
            'data_quality': [quality_validator,
                            toolkit.get_converter('convert_from_extras')],
            'quality_note': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')],
	    'bydata': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')],
            'bydata_email': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')],
            'metadata_id': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')],
        })
        return schema

    def is_fallback(self):
        return True

    def package_types(self):
        return []

    def get_helpers(self):
        return {
            'get_frequency_translation': get_frequency_translation,
            'get_quality_translation': get_quality_translation
        }
    
    def before_map(self, map):
        ''' IRoutes '''
        #Override new dataset so we can optionally skip resource adding
        pkg_ctrl = 'ckanext.cphmetadata.controllers.package:MetadataPackageController'
        home_ctrl = 'ckanext.cphmetadata.controllers.home:MetadataHomeController'
        csv_ctrl = 'ckanext.cphmetadata.controllers.csv:CsvExportController'
        map.connect('add dataset', '/dataset/new', controller=pkg_ctrl, action='new')
        map.connect('home', '/', controller=home_ctrl, action='index')
        map.connect('download csv', '/download', controller=csv_ctrl, action='download')
        return map

