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
 
#orgmap = {
    #"økf": 'ec475e17-45a7-48be-aec9-01d2d516d8fd',#"Økonomiforvaltningen",
    #"buf": 'f1c73fe7-7448-4301-ab04-29b6a640cfcf',#"Børne- og ungdomsforvaltningen",
    #"kff": '0b3d54aa-1f66-4c1b-93e3-1bc7eb6fa2e6',#"Kultur- og Fritidsforvaltningen",
    #"tmf": 'f1f42eb6-2e71-4e2f-ae18-c001b4029f37',#"Teknik- og Miljøforvaltningen",
    #"suf": '7a25a01b-3f25-4b3b-aaa8-71acf58dce1d',#"Sundheds- og omsorgsforvaltningen",
    #"sof": 'a58a461d-7081-43de-b8d2-7718bf1ec0d9',#"Socialforvaltningen",
    #"bif": '21758777-9c28-4072-a913-24a64750c1cb' #"Beskæftigelses- og Integrationsforvaltningen"
#}
orgmap = {
    "økf": '1d1a4698-82d5-4586-bd6b-f6166b8db831',#"Økonomiforvaltningen",
    "buf": '1d1a4698-82d5-4586-bd6b-f6166b8db831',#"Børne- og ungdomsforvaltningen",
    "kff": '1d1a4698-82d5-4586-bd6b-f6166b8db831',#"Kultur- og Fritidsforvaltningen",
    "tmf": '1d1a4698-82d5-4586-bd6b-f6166b8db831',#"Teknik- og Miljøforvaltningen",
    "suf": '1d1a4698-82d5-4586-bd6b-f6166b8db831',#"Sundheds- og omsorgsforvaltningen",
    "sof": '1d1a4698-82d5-4586-bd6b-f6166b8db831',#"Socialforvaltningen",
    "bif": '1d1a4698-82d5-4586-bd6b-f6166b8db831' #"Beskæftigelses- og Integrationsforvaltningen"
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
                'office': hit['center'] if 'center' in hit else None,
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
print("skipped: {0}".format(len(skipped)))
#for skip in skipped:
    #print(skip)
print('---------------------------------------------------------------------')
print("added: {0}".format(len(added)))
for add in added:
    create_dataset(add)
