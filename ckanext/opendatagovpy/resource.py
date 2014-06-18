# -*- coding: utf-8 -*-
#
# @author	Rodrigo Parra
# @copyright	2014 Governance and Democracy Program USAID-CEAMSO
# @license 	http://www.gnu.org/licenses/gpl-2.0.html
#
# USAID-CEAMSO
# Copyright (C) 2014 Governance and Democracy Program
# http://ceamso.org.py/es/proyectos/20-programa-de-democracia-y-gobernabilidad
#
#----------------------------------------------------------------------------
# This file is part of the Governance and Democracy Program USAID-CEAMSO,
# is distributed as free software in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License version 2 as published by the
# Free Software Foundation, accessible from <http://www.gnu.org/licenses/> or write
# to Free Software Foundation (FSF) Inc., 51 Franklin St, Fifth Floor, Boston,
# MA 02111-1301, USA.
#---------------------------------------------------------------------------
# Este archivo es parte del Programa de Democracia y Gobernabilidad USAID-CEAMSO,
# es distribuido como software libre con la esperanza que sea de utilidad,
# pero sin NINGUNA GARANTÍA; sin garantía alguna implícita de ADECUACION a cualquier
# MERCADO o APLICACION EN PARTICULAR. Usted puede redistribuirlo y/o modificarlo
# bajo los términos de la GNU Lesser General Public Licence versión 2 de la Free
# Software Foundation, accesible en <http://www.gnu.org/licenses/> o escriba a la
# Free Software Foundation (FSF) Inc., 51 Franklin St, Fifth Floor, Boston,
# MA 02111-1301, USA.
#
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

