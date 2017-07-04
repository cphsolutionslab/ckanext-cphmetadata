ckanext-cphmetadata
=========
ckanext-cphmetadata is [CKAN](https://github.com/ckan/ckan) extension built for metadata portal managed by [Copenhagen Municipality](https://www.kk.dk/). The extension adds multiple custom fields (update frequency, department, office, etc...) and shortens the dataset creation process to just one step. 

Installing
-------
__NB! This module is developed on CKAN v2.3.1, compatibile with v2.6.3

1) Clone this repo  

```sh
cd /usr/lib/ckan/default/src
git clone https://github.com/cphsolutionslab/ckanext-cphmetadata.git
cd ckanext-cphmetadata
python setup.py develop
sudo nano /etc/ckan/default/production.ini
# Enable plugin in configuration
# ckan.plugins = datastore ... cphmetadata
```
