
__author__ = 'Rodrigo Parra'

import ckan.plugins.toolkit as toolkit
import ckan.plugins as plugins

class ParaguayThemePlugin(plugins.SingletonPlugin):
    '''CKAN Plugin containing theming customizations for a Paraguay CKAN instance.

    '''
    # Declare that this class implements IConfigurer.
    plugins.implements(plugins.IConfigurer)

    def update_config(self, config):

        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        # 'templates' is the path to the templates dir, relative to this
        # plugin.py file.
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_public_directory(config, 'public')
        toolkit.add_resource('fanstatic', 'ckanext-opendatagovpy')
