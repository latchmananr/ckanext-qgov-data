import logging, os

from ckan.plugins import implements, SingletonPlugin, IConfigurer, IRoutes, ITemplateHelpers

LOG = logging.getLogger(__name__)

from ckan.lib.base import h

def beta_or_prod_asset():
    if 'qld.gov.au' in h.full_current_url():
        return 'global/prod-includes/'
    else:
        return 'global/beta-includes/'

def random_tags():
    import random
    tags = h.unselected_facet_items('tags', limit=15)
    random.shuffle(tags)
    return tags

def format_resource_filesize(size):
    import ckan.lib.formatters as formatters
    return formatters.localised_filesize(int(size))

def portal_type(case):
    types = {'ls': 'dataset',
             'lss': 'datasets',
             'us': 'Dataset',
             'uss': 'Datasets',
             'l': 'data',
             'site': 'data',
             'u': 'Data',
             'usite': 'Data'
            }
    return types.get(case)

def group_id_for(group_name):
    import ckan.model as model
    group = model.Group.get(group_name)

    if group and group.is_active():
        return group.id
    else:
        LOG.error("%s group was not found or not active", group_name)
        return None

def user_password_validator(key, data, errors, context):
    from ckan.lib.navl.dictization_functions import Missing
    from pylons import config
    from pylons.i18n import _
    import re

    password_min_length = int(config.get('password_min_length', '10'))
    password_patterns = config.get('password_patterns', r'.*[0-9].*,.*[a-z].*,.*[A-Z].*,.*[-`~!@#$%^&*()_+=|\\/ ].*').split(',')

    value = data[key]

    if value is None or value == '' or isinstance(value, Missing):
        raise ValueError(_('You must provide a password'))
    if not len(value) >= password_min_length:
        errors[('password',)].append(_('Your password must be {min} characters or longer'.format(min=password_min_length)))
    for policy in password_patterns:
        if not re.search(policy, value):
            errors[('password',)].append(_('Must contain at least one number, lowercase letter, capital letter, and symbol'))

class QGOVDataPlugin(SingletonPlugin):
    """Apply custom content and functions for the Open Data portal.

    ``IConfigurer`` allows us to add/modify configuration options.
    ``IRoutes`` allows us to add new URLs, or override existing URLs.
    ``ITemplateHelpers`` allows us to provide helper functions to templates.
    """
    implements(IConfigurer, inherit=True)
    implements(IRoutes, inherit=True)
    implements(ITemplateHelpers, inherit=True)

    def __init__(self, **kwargs):
        import ckan.logic.validators as validators
        validators.user_password_validator = user_password_validator
        import anti_csrf, authenticator
        # Broken in PRD; disable and then fix properly in staging.
        #anti_csrf.intercept_csrf()
        authenticator.intercept_authenticator()

    def get_helpers(self):
        """ A dictionary of extra helpers that will be available
        to provide QGOV-specific helpers to the templates.
        """
        from ckanext.qgov.data.stats import Stats

        helper_dict = {}
        helper_dict['beta_or_prod_asset'] = beta_or_prod_asset
        helper_dict['random_tags'] = random_tags
        helper_dict['portal_type'] = portal_type
        helper_dict['group_id_for'] = group_id_for
        helper_dict['format_resource_filesize'] = format_resource_filesize
        helper_dict['top_organisations'] = Stats.top_organisations
        helper_dict['top_categories'] = Stats.top_categories
        helper_dict['resource_count'] = Stats.resource_count
        helper_dict['resource_report'] = Stats.resource_report
        helper_dict['resource_org_count'] = Stats.resource_org_count

        return helper_dict

    def update_config(self, config):
        """This IConfigurer implementation causes CKAN to look in the
        ```public``` and ```templates``` directories present in this
        package for any customisations.
        """
        here = os.path.dirname(__file__)
        our_public_dir = '/srv/data/public'
        template_dir = '/srv/data/templates,'+os.path.join(here, 'theme', 'templates')

        # set our local template and resource overrides
        # ensure that our resources take precedence over all other plugins
        config['extra_public_paths'] = our_public_dir + ',' + config['extra_public_paths']
        config['extra_template_paths'] = template_dir + ',' + config['extra_template_paths']
        config['licenses_group_url'] = 'file://'+os.path.join(here, 'resources', 'qgov-licences.json')
        config['ckan.template_title_deliminater'] = '|'

        # block unwanted content
        config['openid_enabled'] = False
        return config

    def before_map(self, routeMap):
        """ Use our custom controller, and disable some unwanted URLs """
        controller = 'ckanext.qgov.data.controller:QGOVDataController'
        routeMap.connect('/announcements', controller=controller, action='announcements')
        routeMap.connect('/contact', controller=controller, action='contact')
        routeMap.connect('/feedback', controller=controller, action='feedback')
        routeMap.connect('/maps-geospatial', controller=controller, action='mapsGeospatial')
        routeMap.connect('/request-data', controller=controller, action='requestData')
        routeMap.connect('/thanks', controller=controller, action='thanks')
        routeMap.connect('/other-data', controller=controller, action='otherData')
        routeMap.connect('/data-event', controller=controller, action='dataEvent')
        routeMap.connect('/data-event/premiers-awards', controller=controller, action='dataEventPremiersAwards')
        routeMap.connect('/data-event/opening-the-vault', controller=controller, action='dataEventOpeningTheVault')
        routeMap.connect('/data-event/microsoft-masterclass', controller=controller, action='dataEventMicrosoftMasterclass')
        routeMap.connect('/data-event/govhack-2014', controller=controller, action='dataEventGovHack2014')
        routeMap.connect('/maps-geospatial/qld-globe', controller=controller, action='mapsGeospatialGlobe')
        routeMap.connect('/department-strategies', controller=controller, action='departmentStrategies')
        routeMap.connect('/department-strategies/about', controller=controller, action='departmentStrategiesAbout')
        routeMap.connect('/storage/upload_handle', controller=controller, action='upload_handle')
        routeMap.connect('/user/logged_in', controller=controller, action='logged_in')
        routeMap.connect('/data-event/premiers-awards/about', controller=controller, action='dataPremierAwardAbout')
        routeMap.connect('/data-event/premiers-awards/about-2013', controller=controller, action='dataPremierAwardAbout2013')
        routeMap.connect('/data-event/premiers-awards/events', controller=controller, action='dataPremierAwardEvents')
        routeMap.connect('/data-event/premiers-awards/guidelines', controller=controller, action='dataPremierAwardGuidelines')
        routeMap.connect('/for-developers', controller=controller, action='forDevelopers')
        routeMap.connect('/for-developers/register-your-app', controller=controller, action='forDevelopersRegisterYourApp')
        routeMap.connect('/case-studies', controller=controller, action='caseStudies')
        routeMap.connect('/case-studies/weather-data', controller=controller, action='caseStudiesWeatherData')
        routeMap.connect('/case-studies/wildlife-data', controller=controller, action='caseStudiesWildlifeData')
        routeMap.connect('/case-studies/multiple-soil-datasets', controller=controller, action='caseStudiesMultipleSoilDatasets')
        routeMap.connect('/case-studies/qld-school-zones', controller=controller, action='caseStudiesQldSchoolZones')
        routeMap.connect('/case-studies/pocket-zoner', controller=controller, action='caseStudiesPocketZoner')
        routeMap.connect('/case-studies/brisbane-bus-train-app', controller=controller, action='caseStudiesBrisbaneBusTrainApp')

        routeMap.connect('/static-content/{path:[-_a-zA-Z0-9/]+}', controller=controller, action='static_content')

        # block unwanted content
        routeMap.connect('/user', controller='error', action='404')
        routeMap.connect('/user/register', controller='error', action='404')
        routeMap.connect('/user/followers/{username:.*}', controller='error', action='404')
        routeMap.connect('/api/action/follow{action:.*}', controller='error', action='404')
        return routeMap
