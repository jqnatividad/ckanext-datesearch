# ckanext-relation
This extension provides temporal search for those datasets which have a date range for the period in which they are collected or carried out (archive or real-time).

This code is inspired by these [sources](#acknowledgement).


## Requirements


This extension is tested with CKAN 2.8.0.

You may need to check you schema.xml to see that this line exists:
```
<dynamicField name="extras_*" type="text" indexed="true" stored="true" multiValued="false"/>
```

If you use the default ckan metadata, as extra field you may add two (or only one of them) attributes (key): "begin-collection_date" and "end-collection_date".
In case you use ckanext-scheming, then you need to add these two fields into your schema json file.


The main part of the code is located at [plugin.py](/ckanext/datesearch/plugin.py) at `before_search`. There exist three conditions for the date range search:
* where both start and end date are given in the search field
* where only the start date is given in the search field
* where only the end date is given in the search field
in all these conditions, we look at the datasets which have either both or any of begin or end collection date.
Here is the complete code:
```
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
```



## Installation

To install ckanext-relation:

1. Activate your CKAN virtual environment, for example::

       . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-datesearch Python package into your virtual environment::

       pip install -e 'git+https://github.com/MandanaMoshref/ckanext-datesearch.git#egg=ckanext-datesearch'

3. Add ``datesearch`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

       sudo service apache2 reload



## Developer installation

To install ckanext-relation for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/MandanaMoshref/ckanext-datesearch.git
    cd ckanext-relation
    python setup.py develop


## License
The ckanext-datesearch is available as free and open source and is licensed under the GNU Affero General Public License version 3 (AGPLv3)
** This code contains some external libraries such as:
- [Moment.js](http://momentjs.com/), MIT License

## Acknowledgement
This code is an follow-up from the [CKAN issue #5021](https://github.com/ckan/ckan/issues/5021). 
It is an adaptation of temporal search from [ckanext-tsbsatellites](https://github.com/okfn/ckanext-tsbsatellites).
