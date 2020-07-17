from datetime import date, datetime
import json
import logging


import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


import ckanext.datesearch.helpers as helpers


log = logging.getLogger(__name__)


class DateSearchPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)

    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_resource('fanstatic/resources', 'ckanext-datesearch')


    # ITemplateHelpers

    def get_helpers(self):
        return {
                'get_default_slider_values':helpers.get_default_slider_values,
                'get_date_url_param': helpers.get_date_url_param,
                }



    def before_search(self, search_params):

        today = datetime.today()
        past = datetime.strptime('1990-01-01', '%Y-%m-%d')
        
        def parse_date(date_string):
            '''
            Parse a date string or throw a nice error into the log. Re-raises
            the error for the plugin to catch.
            '''
            try:
                return datetime.strptime(date_string, '%Y-%m-%d')
            except ValueError as e:
                log.debug('Date {0} not in the right format. Needs to be YYYY'
                        '-MM-DD'.format(date_string))
                raise e        
        
        if (search_params.get('extras', None) and 'ext_begin_date' in
                search_params['extras'] and 'ext_end_date' in
                search_params['extras']):
            try:
                begin = parse_date(search_params['extras']['ext_begin_date'])
                end = parse_date(search_params['extras']['ext_end_date'])
            except ValueError:
                return search_params
            # Adding 'Z' manually here is evil, but we do this in core too.
            query = '(begin-collection_date:[ * TO {1}Z] -end_collection_date:[* TO *]) OR (-begin-collection_date:[ * TO * ] -end_collection_date:[ {0}Z TO *]) OR (begin-collection_date:[ * TO {1}Z] end_collection_date:[{0}Z TO *])'
            query = query.format(begin.isoformat(), end.isoformat())
            search_params['fq'] = query
        
        elif (search_params.get('extras') and 'ext_begin_date' not in
                search_params['extras'] and 'ext_end_date' in
                search_params['extras']):
            try:
                begin = past
                end = parse_date(search_params['extras']['ext_end_date'])
            except ValueError:
                return search_params
            # Adding 'Z' manually here is evil, but we do this in core too.
            query = '(begin-collection_date:[ * TO {1}Z] -end_collection_date:[* TO *]) OR (-begin-collection_date:[ * TO * ] -end_collection_date:[ {0}Z TO *]) OR (begin-collection_date:[ * TO {1}Z] end_collection_date:[{0}Z TO *])'
            query = query.format(begin.isoformat(), end.isoformat())
            search_params['fq'] = query
        
        elif (search_params.get('extras') and 'ext_begin_date' in
        search_params['extras'] and 'ext_end_date' not in
        search_params['extras']):
            try:
                begin = parse_date(search_params['extras']['ext_begin_date'])
                end = today
            except ValueError:
                return search_params
            # Adding 'Z' manually here is evil, but we do this in core too.
            query = '(begin-collection_date:[ * TO {1}Z] -end_collection_date:[* TO *]) OR (-begin-collection_date:[ * TO * ] -end_collection_date:[ {0}Z TO *]) OR (begin-collection_date:[ * TO {1}Z] end_collection_date:[{0}Z TO *])'
            query = query.format(begin.isoformat(), end.isoformat())
            search_params['fq'] = query
        return search_params
        

'''
    def before_index(self, data_dict):

        # Do not index the collection date fields if the date is null
        # This should be fixed in core in ckan/ckan#1701
        package_dict = json.loads(data_dict['data_dict'])
        for field in ('begin-collection_date', 'end-collection_date',):
            for extra in package_dict.get('extras', []):
                if extra['key'] == field and not extra['value']:
                    data_dict.pop(field, None)

        return data_dict
'''








