'''This script will import data from json file into CKAN via API'''
import json
import requests
import unidecode

freqmap = {
    'dagligt': 'daily',
    'ugentligt': 'weekly',
    'månedligt': 'monthly',
    'sporadisk': 'infrequently',
    'årligt': 'annually',
    'halvårligt': 'biannually',
    'aldrig': 'never'
}
 
orgmap = {
    "økf": '9388a364-a0d8-42dc-9d2b-2ab3b152d635',#"Økonomiforvaltningen",
    "buf": 'a5976f1f-5abe-4891-8143-c700bf578893',#"Børne- og ungdomsforvaltningen",
    "kff": '50bd6e51-419c-4b23-8750-3fd88f80c183',#"Kultur- og Fritidsforvaltningen",
    "tmf": 'd3e86e5a-a1da-440a-a660-bd28743f3f0b',#"Teknik- og Miljøforvaltningen",
    "suf": 'a76829d4-d3b3-42e0-9d9c-9be93a5cc19e',#"Sundheds- og omsorgsforvaltningen",
    "sof": '02969b0d-99e9-4be2-92f3-c5cd6d432c5a',#"Socialforvaltningen",
    "bif": 'ca02cfc6-c977-49b1-9f29-fa31d02b34c7' #"Beskæftigelses- og Integrationsforvaltningen"
}
skipped = []
added = []
def parse_data():
    with open('data.json') as datasets:
        data = json.load(datasets)
        for hit in data['rows']:
            #Weed out wrong data
            if 'type' in hit['doc'] and hit['doc']['type'] != 'data':
                skipped.append(hit)
                continue
            if 'properties' not in hit['doc']:
                skipped.append(hit)
                continue
            hit = hit['doc']['properties']
            if 'forvaltning' not in hit:
                skipped.append(hit)
                continue
            #Defaults for missing data
            if 'opdateringsfrekvens' not in hit:
                #adding 'never' as update frequency
                hit['opdateringsfrekvens'] = 'aldrig'
            if 'data' not in hit:
                hit['data'] = {
                     'Eksternt på data.kk.dk': False,
                     'Internt på KKkort': False,
                     'Eksternt på Københavnerkortet': False,
                 }
            parsed = {
                'name': hit['datasætnavn'],
                'title': hit['titel'],
                'notes': hit['beskrivelse'] if 'beskrivelse' in hit else None,
                'editor': hit['redigering'] if 'redigering' in hit else None,
                'tag_string': hit['tags'] if 'tags' in hit else None,
                'update_frequency': freqmap[hit['opdateringsfrekvens']],
                'maintainer': hit['kontaktperson'] if 'kontaktperson' in hit else None,
                'maintainer_email': hit['kontakt e-mail'] if 'kontakt e-mail' in hit else None,
                'author': hit['dataejer'] if 'dataejer' in hit else None,
                'owner_org': orgmap[hit['forvaltning']],
                'department': hit['afdeling'] if 'afdeling' in hit else None,
                'office': hit['enhed'] if 'enhed' in hit else None,
                'datakk': 'True' if ('Eksternt på data.kk.dk' in hit['data'] and hit['data']['Eksternt på data.kk.dk']) else None,
                'kkkort': 'True' if ('Internt på KKkort' in hit['data'] and hit['data']['Internt på KKkort']) else None,
                'copenhagenkortet': 'True' if ('Eksternt på Københavnerkortet' in hit['data'] and hit['data']['Eksternt på Københavnerkortet']) else None,
            }
            #remove None values
            metadata = dict((k, v) for k, v in parsed.items() if v)
            added.append(metadata)

# Put the details of the dataset we're going to create into a dict.
def create_dataset(data):
    print('Inserting dataset!')
    url = 'http://metadata.bydata.dk/api/action/package_create'
    headers = {
        'Authorization': 'api-key-here',
        'Content-type': 'application/json'
    }
    req = requests.post(url, json.dumps(data), headers=headers)
    print(req.__dict__)

parse_data()
print('---------------------------------------------------------------------')
print("added: {0}".format(len(added)))
for add in added:
    create_dataset(add)
