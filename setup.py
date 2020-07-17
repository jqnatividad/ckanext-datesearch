from setuptools import setup, find_packages

setup(
    name='ckanext-datesearch',
    version='1.0',
    description='CKAN extension for temporal search. This version of implementation is inspired from a part of the "ckanext-tsbsatellites"',
    long_description=
    '''
    ''',
    classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='ckan ckanext datesearch',
    author='Mandana Moshrefzadeh',
    author_email='mandana.moshrefzadeh@tum.de',
    url='https://github.com/mandanamoshref/ckanext-datesearch',
    license='AGPLv3',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points=
    '''
    [ckan.plugins]
    datesearch=ckanext.datesearch.plugin:DateSearchPlugin
    ''',
)
