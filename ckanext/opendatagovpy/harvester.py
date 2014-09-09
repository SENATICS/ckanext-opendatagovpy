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
# ----------------------------------------------------------------------------
# This file is part of the Governance and Democracy Program USAID-CEAMSO,
# is distributed as free software in the hope that it will be useful, but WITHOUT 
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS 
# FOR A PARTICULAR PURPOSE. You can redistribute it and/or modify it under the 
# terms of the GNU Lesser General Public License version 2 as published by the 
# Free Software Foundation, accessible from <http://www.gnu.org/licenses/> or write 
# to Free Software Foundation (FSF) Inc., 51 Franklin St, Fifth Floor, Boston, 
# MA 02111-1301, USA.
# ---------------------------------------------------------------------------
# Este archivo es parte del Programa de Democracia y Gobernabilidad USAID-CEAMSO,
# es distribuido como software libre con la esperanza que sea de utilidad,
# pero sin NINGUNA GARANTÍA; sin garantía alguna implícita de ADECUACION a cualquier
# MERCADO o APLICACION EN PARTICULAR. Usted puede redistribuirlo y/o modificarlo 
# bajo los términos de la GNU Lesser General Public Licence versión 2 de la Free 
# Software Foundation, accesible en <http://www.gnu.org/licenses/> o escriba a la 
# Free Software Foundation (FSF) Inc., 51 Franklin St, Fifth Floor, Boston, 
# MA 02111-1301, USA.
#
import json
from ckan.plugins import SingletonPlugin, implements
from ckanext.harvest.harvesters import CKANHarvester
import logging
from ckanext.harvest.interfaces import IHarvester

log = logging.getLogger(__name__)

__author__ = 'Rodrigo Parra'


class ParaguayCKANHarvester(CKANHarvester, SingletonPlugin):
    implements(IHarvester)

    def info(self):
        return {
            'name': 'paraguay-harvester',
            'title': 'Paraguay CKAN Harvester',
            'description': 'A custom CKAN harvester for OpenDataGovPy'
            }

    def import_stage(self, harvest_object):
        log.debug('In ParaguayCKANHarvester import_stage')

        pkg_dict = json.loads(harvest_object.content)
        log.debug('Paraguay Harvest: %r', pkg_dict)
        if not pkg_dict.get('type') == 'harvest':
            pkg_dict['private'] = True
            harvest_object.content = json.dumps(pkg_dict)
            log.debug('Paraguay Harvest probanddoooo 1: %r', pkg_dict)

        return super(ParaguayCKANHarvester, self).import_stage(harvest_object)

    # def gather_stage(self,harvest_job):
    #     log.debug('In ParaguayCKANHarvester gather_stage')
    #     return 1
    #
    # def fetch_stage(self,harvest_object):
    #     log.debug('In ParaguayCKANHarvester fetch_stage')
    #     return True