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

from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
    name='ckanext-opendatagovpy',
    version=version,
    description="CKAN Extension with containing customizations for a Paraguay CKAN instance.",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Rodrigo Parra',
    author_email='rodpar07@gmail.com',
    url='',
    license='Affero GPL',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.opendatagovpy'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points='''
        [ckan.plugins]
        opendatagovpy_theme=ckanext.opendatagovpy.theme:ParaguayThemePlugin
        opendatagovpy_dataset = ckanext.opendatagovpy.dataset:ParaguayDatasetFormPlugin
        opendatagovpy_resource = ckanext.opendatagovpy.resource:ParaguayResourceFormPlugin
        paraguay_harvester = ckanext.opendatagovpy.harvester:ParaguayCKANHarvester

        [paste.paster_command]
        translations=ckanext.opendatagovpy.translation:TranslationsCommand
    ''',
)
