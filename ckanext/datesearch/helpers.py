import ckan.lib.helpers as h
import ckan.plugins as p
import ckan.plugins.toolkit as tk
import datetime
import json


def get_default_slider_values():
    '''Returns the earliest collection date from package_search'''

    data_dict = {
            'sort': 'begin-collection_date asc',
            'rows': 1,
            'q': 'begin-collection_date:[* TO *]',
    }
    result = p.toolkit.get_action('package_search')({}, data_dict)['results']

    if len(result) == 1:
        #date = filter(lambda x: x['key'] == 'begin-collection_date', result[0].get('extras', []))
        #begin = date[0]['value']
        date = (result[0].get('begin-collection_date', []))
        begin = date
        
    else:
        begin = datetime.date.today().isoformat()

    
    data_dict = {
            'sort': 'end-collection_date desc',
            'rows': 1,
            'q': 'end-collection_date:[* TO *]',
    }
    result = p.toolkit.get_action('package_search')({}, data_dict)['results']
    #print(end_collection_date)

    if len(result) == 1:
        #date = filter(lambda x: x['key'] == 'end-collection_date', result[0].get('extras', []))    
        #end = date[0]['value']
        date = (result[0].get('end-collection_date', []))
        end = date
    else:
        end = datetime.date.today().isoformat()
    return begin, end



def get_date_url_param():
    params = ['', '']
    for k, v in tk.request.params.items():
        if k == 'ext_begin_date':
            params[0] = v
        elif k == 'ext_end_date':
            params[1] = v
        else:
            continue
    return params

