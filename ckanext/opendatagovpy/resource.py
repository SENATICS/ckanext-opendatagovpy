__author__ = 'Rodrigo Parra'

import ckan.plugins as plugins
import json
from logging import getLogger

log = getLogger(__name__)


class ParaguayResourceFormPlugin(plugins.SingletonPlugin):
    """
    Custom Resource form.
    """
    plugins.implements(plugins.IResourceController)
    plugins.implements(plugins.ITemplateHelpers)

    _schema_fields = []
    _dynamic_fields = []


    def get_helpers(self):
        return {
            'dpy_get_schema_fields': self._get_schema_fields,
            'dpy_get_dynamic_fields': self._get_dynamic_fields
        }

    def _get_schema_fields(self):
        return self._schema_fields

    def _get_dynamic_fields(self):
        return self._dynamic_fields

    def is_fallback(self):
        return True

    def package_types(self):
        return []

    def before_show(self, resource_dict):
        if 'schema' in resource_dict:
            try:
                self._schema_fields = json.loads(resource_dict['schema'])['fields']
                log.debug('Cargando schema')
                log.debug(self._schema_fields)
            except ValueError:
                log.info("Entry 'schema' is not valid JSON. This should not happen.")
            except KeyError:
                log.info("Entry 'schema' does not have 'fields' attribute. This is mandatory JSON Table Schema syntax.")
        else:
            self._schema_fields = []

        if 'dynamic' in resource_dict:
            try:
                self._dynamic_fields = json.loads(resource_dict['dynamic'])
            except ValueError:
                log.info("Entry 'schema' is not valid JSON. This should not happen.")
            except KeyError:
                log.info("Entry 'schema' does not have 'fields' attribute. This is mandatory JSON Table Schema syntax.")
        else:
            self._dynamic_fields = []
        return resource_dict

