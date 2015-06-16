# -*- coding: utf-8 -*-
#
# @author	Verena Ojeda
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
__author__ = 'Verena Ojeda'

from webhelpers.html import escape
import ckan.plugins.toolkit as t
import ckan.plugins as plugins
from logging import getLogger
from pylons import config
import ckan.model as model
import datetime
import re
from ckanext.qa import reports
from ckan.common import _

log = getLogger(__name__)

def get_caption(num_stars):
    captions = [
        _('Unavailable or not openly licensed'),
        _('Unstructured data (e.g. PDF)'),
        _('Structured data but proprietry format (e.g. Excel)'),
        _('Structured data in open format (e.g. CSV)'),
        _('Linkable data - served at URIs (e.g. RDF)'),
        _('Linked data - data URIs and linked to other data (e.g. RDF)')
        ]
    return captions[num_stars]


def render_datestamp(datestamp_str, format='%d/%m/%Y'):
    # e.g. '2012-06-12T17:33:02.884649' returns '12/6/2012'
    if not datestamp_str:
        return ''
    try:
        return datetime.datetime(*map(int, re.split('[^\d]', datestamp_str)[:-1])).strftime(format)
    except Exception:
        return ''


# Openness Score Facet
def mini_stars_facet(num_stars):
    '''
    Returns HTML for a numbers of mini-stars with a caption describing the meaning.
    '''
    mini_stars = num_stars * '&#9733'
    mini_stars += '&#9734' * (5-num_stars)
    caption = get_caption[int(num_stars)]
    return t.literal('%s&nbsp; %s' % (mini_stars, caption))


def mini_stars_and_caption(num_stars):
    '''
    Returns HTML for a numbers of mini-stars with a caption describing the meaning.
    '''
    mini_stars = num_stars * '&#9733'
    mini_stars += '&#9734' * (5-num_stars)
    caption = [
        _('Unavailable or not openly licensed'),
        _('Unstructured data (e.g. PDF)'),
        _('Structured data but proprietry format (e.g. Excel)'),
        _('Structured data in open format (e.g. CSV)'),
        _('Linkable data - served at URIs (e.g. RDF)'),
        _('Linked data - data URIs and linked to other data (e.g. RDF)')
    ]
    #log.debug(caption[num_stars])
    return t.literal('%s&nbsp; %s' % (mini_stars, caption[num_stars]))


def render_stars(stars, reason, last_updated):
    '''Returns HTML to show a number of stars out of five, with a reason and
    date, plus a tooltip describing the levels.'''

    if stars==0:
        stars_html = 5 * '<i class="icon-star-empty"></i>'
    else:
        stars_html = (stars or 0) * '<i class="icon-star"></i>'
        stars_html += (5-stars) * '<i class="icon-star-empty"></i>'

    tooltip = t.literal('<div class="star-rating-reason"><b>' + _('Reason') + ': </b>%s</div>' % escape(_(reason))) if reason else ''
    for i in range(5,0,-1):
        classname = 'fail' if (i > (stars or 0)) else ''
        tooltip += t.literal('<div class="star-rating-entry %s">%s</div>' % (classname, mini_stars_and_caption(i)))

    if last_updated:
        datestamp = render_datestamp(last_updated)
        tooltip += t.literal('<div class="star-rating-last-updated"><b>' + _('Score updated') + ': </b>%s</div>' % datestamp)


    tooltipo = t.literal(_('Reason') + ': %s' % _(reason)) if reason else ''

    for i in range(5,0,-1):
        tooltipo += t.literal("&#xa;%s" % mini_stars_and_caption(i))

    if last_updated:
        datestamp = render_datestamp(last_updated)
        tooltipo += t.literal(_('Score updated') + ' %s' % datestamp)

    return t.literal(_('Openness Rating') + ': <span class="star-rating"><span class="tooltip" style="display:none">%s</span>'
                                            '<a href="http://lab.linkeddata.deri.ie/2010/star-scheme-by-example/" target="_blank">%s</a>'
                                            '</span>' % (tooltip, stars_html))
    #log.debug(t.literal(_('Openness Rating') + ': <span data-tooltip="%s" class="tooltip-top">%s</span>' % (tooltipo, stars_html)))
    #return t.literal(_('Openness Rating') + ': <span data-tooltip="%s" class="tooltip-right">%s</span>' % (tooltipo, stars_html))

def render_mini_stars(stars):
    '''Returns HTML to show a number of stars out of five, with a reason and
    date, plus a tooltip describing the levels.'''

    if stars==0:
        stars_html = 5 * '&#9734'
    else:
        stars_html = (int(stars) or 0) * '&#9733'
        stars_html += (5-int(stars)) * '&#9734'

    reason = get_caption(int(stars))
    tooltip = t.literal('<div class="star-rating-reason">%s</div>' % escape(reason)) if reason else ''

    return t.literal('<span class="star-rating"><span class="tooltip">%s</span>%s</span>' % (tooltip, stars_html))
    #return t.literal('<span data-tooltip="%s" class="tooltip-right">%s</span>' % (escape(reason), stars_html))


def is_plugin_enabled(plugin_name):
    return plugin_name in config.get('ckan.plugins', '').split()


## Metodos usados para renderizar rating e info sobre el nivel  de estrellas en la vista de datasets
def openness_new_get_star_html(dataset_id):
    extra_vars = get_dataset_openness(dataset_id)
    return plugins.toolkit.literal(plugins.toolkit.render('package/snippets/stars_dataset_module.html',
                             extra_vars=extra_vars))


def get_dataset_openness(dataset_id):
    # Obtener el mayor report de todos los resource del dataset
    #report = reports.five_stars(dataset_id)
    dataset_report = five_stars(dataset_id)
    id_max_resource = ''
    max_star = 0
    stars = 0
    reason = plugins.toolkit._('Not Rated')
    updated = ""
    for resource in dataset_report:
        if resource.get('openness_score', -1) > max_star:
            max_star = resource.get('openness_score', -1)
            id_max_resource = resource.get('resource_id','')

    if id_max_resource:
        resource_report = reports.resource_five_stars(id_max_resource)
        stars = resource_report.get('openness_score', -1)
        updated = resource_report.get('openness_updated')

        if stars >= 0:
            reason = resource_report.get('openness_score_reason')

    extra_vars = {'stars': stars, 'reason': reason, 'updated': updated}
    return extra_vars


def get_resource_openness(resource_id):
    stars = 0
    reason = plugins.toolkit._('Not Rated')
    updated = ""

    if resource_id:
        resource_report = reports.resource_five_stars(resource_id)
        stars = resource_report.get('openness_score', -1)
        updated = resource_report.get('openness_updated')

        if stars >= 0:
            reason = resource_report.get('openness_score_reason')

    extra_vars = {'stars': stars, 'reason': reason, 'updated': updated}
    return extra_vars


def five_stars(id=None):
    """
    Return a list of dicts: 1 for each dataset that has an openness score.

    Each dict is of the form:
        {'name': <string>, 'title': <string>, 'openness_score': <int>}
    """
    #log.debug(id)
    if id:
        pkg = model.Package.get(id)
        #log.debug(pkg)
        if not pkg:
            return "Not found"

    # take the maximum openness score among dataset resources to be the
    # overall dataset openness core
    query = model.Session.query(model.Package.name, model.Package.title,
                                model.Resource.id,
                                model.TaskStatus.value.label('value'))
    query = reports._join_package_to_resource_group_if_it_exists(query)
    query = query \
        .join(model.Resource)\
        .join(model.TaskStatus, model.TaskStatus.entity_id == model.Resource.id)\
        .filter(model.TaskStatus.key==u'openness_score')\
        .group_by(model.Package.name, model.Package.title, model.Resource.id, model.TaskStatus.value)\
        .distinct()

    if id:
        query = query.filter(model.Package.id == pkg.id)

    results = []
    for row in query:
        results.append({
            'name': row.name,
            'title': row.title + u' ' + row.id,
            'resource_id': row.id,
            'openness_score': row.value
        })
    return results

try:
    from collections import OrderedDict
except ImportError:
    from sqlalchemy.util import OrderedDict


def get_facet_fields():
    # Return fields that we'd like to add to default CKAN faceting.
    facets = OrderedDict()
    facets["extras_openness_score"] = _('Openness Score')
    #facets["maintainer"] = _('Openness')
    return facets


class ParaguayOpennessPlugin(plugins.SingletonPlugin):
    """
    Custom Resource form.
    """
    #plugins.implements(plugins.IResourceController)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.interfaces.IFacets)

    # ITemplateHelpers

    def get_helpers(self):
        '''Register the most_popular_groups() function above as a template
        helper function.
        '''
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.

        helper_dict = {'openness_stars': openness_new_get_star_html,
                       'get_dataset_openness': get_dataset_openness,
                       'get_resource_openness': get_resource_openness,
                       'mini_stars_and_caption': mini_stars_and_caption,
                       'render_stars': render_stars,
                       'render_mini_stars': render_mini_stars}

        return helper_dict

    # IFacets

    def dataset_facets(self, facets, package_type):
        # Add any facets specified in package_to_pod.get_facet_fields() to the top
        # of the facet list, and then put the CKAN default facets below that.
        f = OrderedDict()
        f.update(get_facet_fields())
        f.update(facets)
        return f


    def group_facets(self, facets_dict, group_type, package_type):
        return facets_dict


    def organization_facets(self, facets_dict, organization_type, package_type):
        return facets_dict

