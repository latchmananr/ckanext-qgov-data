from setuptools import setup, find_packages

version='@BUILD-LABEL@'

setup(
    name='ckanext-qgov-data',
    version=version,
    description='Adds Queensland Government custom content',
    long_description='',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Online Enabling Solutions',
    author_email='osidt@dsiti.qld.gov.au',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.qgov', 'ckanext.qgov.data'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    entry_points=\
    """
    [ckan.plugins]
    qgovdata=ckanext.qgov.data.plugin:QGOVDataPlugin
    """,
)
