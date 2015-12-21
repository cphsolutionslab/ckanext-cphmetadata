import os
import pylons
import inspect
import losser.losser
from ckan.logic import get_action
from ckanext.cphmetadata.plugin import get_quality_translation, get_frequency_translation
from ckan.controllers.admin import AdminController

class CsvExportController(AdminController):
    """This controller exports datasets to a CSV file. Requires sysadmin role to download as private datasets are also included"""

    def _absolute_path(self, relative_path):
        """Return an absolute path given a path relative to this Python file."""
        return os.path.join(os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe()))), relative_path)

    def transform(self, results):
        """Prepares JSON values for CSV export."""
        for result in results:
            result['tags'] = [tag['display_name'] for tag in result['tags']]
            if result['organization']:
                result['organization'] = result['organization']['title']
            if 'update_frequency' in result:
                result['update_frequency'] = get_frequency_translation(result['update_frequency'])
            if 'data_quality' in result:
                result['data_quality'] = get_quality_translation(result['data_quality'])

    def download(self):
        """Uses package_search action to get all datasets in JSON format and transform to CSV"""
        context = {
            'ignore_capacity_check': True #Includes private datasets
        }
        search_results = get_action('package_search')(context, {'rows': 1000000})
        results = search_results['results']

        self.transform(results)

        #Load CSV columns from JSON file
        columns = self._absolute_path('../../../columns.json')
        csv_string = losser.losser.table(results, columns, csv=True, pretty=False)

        pylons.response.headers['Content-Type'] = 'text/csv;charset=utf-8'
        pylons.response.headers['Content-Disposition'] = 'attachment; filename="metadata.csv"'
        return csv_string
