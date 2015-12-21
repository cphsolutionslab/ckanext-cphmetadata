#!/usr/bin/python
# -*- coding: utf-8 -*-
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h
from ckan.plugins.toolkit import Invalid
import datetime

def frequency_validator(value, context):
    if value not in ['daily', 'weekly', 'monthly', 'biannually', 'annually', 'infrequently', 'never', 'never_actual']:
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
    freqmap = {
        'daily': 'Daily',
        'weekly': 'Weekly',
        'monthly': 'Monthly',
        'biannually': 'Biannually',
        'annually': 'Annually',
        'infrequently': 'Infrequently',
        'never': '',
        'never_actual': 'Never'
    }
    return freqmap.get(frequency, '')

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
            'update_frequency': [frequency_validator,
                            toolkit.get_converter('convert_to_extras')],
            'department': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'office': [toolkit.get_validator('ignore_missing'),
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
        })
        return schema

    def update_package_schema(self):
        schema = super(CphmetadataPlugin, self).update_package_schema()
        #our custom fields
        schema.update({
            'update_frequency': [frequency_validator,
                            toolkit.get_converter('convert_to_extras')],
            'department': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
            'office': [toolkit.get_validator('ignore_missing'),
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
        })
        return schema

    def show_package_schema(self):
        schema = super(CphmetadataPlugin, self).show_package_schema()
        schema.update({
            'custom_text': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')],
            'update_frequency': [frequency_validator,
                            toolkit.get_converter('convert_from_extras')],
            'department': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')],
            'office': [toolkit.get_converter('convert_from_extras'),
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

