#!/usr/bin/env python

# The Topic Browser
# Copyright 2010-2011 Brigham Young University
#
# This file is part of the Topic Browser <http://nlp.cs.byu.edu/topic_browser>.
#
# The Topic Browser is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# The Topic Browser is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License
# for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with the Topic Browser.  If not, see <http://www.gnu.org/licenses/>.
#
# If you have inquiries regarding any further use of the Topic Browser, please
# contact the Copyright Licensing Office, Brigham Young University, 3760 HBLL,
# Provo, UT 84602, (801) 422-9339 or 422-3821, e-mail copyright@byu.edu.


from django.shortcuts import render_to_response
from django.http import HttpResponse

from topic_modeling.visualize.charts import plot_types
from topic_modeling.visualize.common import BreadCrumb, root_context
from topic_modeling.visualize.models import Analysis
from topic_modeling.visualize.models import Attribute
from topic_modeling.visualize.models import Dataset


def index(request, dataset, analysis, plot):
    plots = plot_types.keys()
    plots.sort(key=lambda x: plot_types[x][1])
    if not plot:
        plot = plots[0]
    context = root_context(dataset, analysis)
    context['highlight'] = 'plots_tab'
    context['tab'] = 'plot'
    context['plot'] = plot

    dataset = Dataset.objects.get(name=dataset)
    analysis = Analysis.objects.get(dataset=dataset, name=analysis)
    context['breadcrumb'] = BreadCrumb()
    context['breadcrumb'].dataset(dataset)
    context['breadcrumb'].analysis(analysis)
    context['breadcrumb'].plot()

    attributes = Attribute.objects.filter(dataset=dataset)
    plot_form = plot_types[plot][0].form(dataset, analysis)
    topics = [analysis.topic_set.all()[0]]
    attribute = attributes[0]
    values = attributes[0].value_set.all()

    topic_links = [context['topics_url'] + '/%s' % str(topic.number)
                   for topic in topics]
    topic_names = [topic.name for topic in topics]
    context['topic_links'] = zip(topic_links, topic_names)

    attr_links = [context['attributes_url'] + '/%s/values/%s' % \
                  (str(attribute), str(value)) for value in values]
    attr_names = [value.value for value in values]
    context['attr_links'] = zip(attr_links, attr_names)



    context['plots'] = plots
    # Needs to be fixed if we ever have lots of kinds of plots
    context['num_pages'] = 1
    context['page_num'] = 1
    context['update_function'] = plot_types[plot][0].update_function

    context['curplot'] = plot
    
    context['plot_form'] = plot_form

    return render_to_response('plot.html', context)


def create_plot_image(request, chart_type, dataset, analysis, attribute,
        topic, value):
    """
    Handles the creation of a topic/nominal attribute plot.  Generates
    the correct plot data and returns the image data to the client in an
    HTTP response.
    """
    chart_parameters = {'dataset': dataset,
                        'analysis': analysis,
                        'attribute': attribute,
                        'topic': topic,
                        'value': value}
    if request.GET.get('frequency', False):
        chart_parameters['frequency'] = 'True'
    if request.GET.get('histogram', False):
        chart_parameters['histogram'] = 'True'
    if request.GET.get('normalized', False):
        chart_parameters['normalized'] = 'True'
    if request.GET.get('kde', False):
        chart_parameters['kde'] = 'True'
    if request.GET.get('points', False):
        chart_parameters['points'] = 'True'

    chart = plot_types[chart_type][0](chart_parameters)

    return HttpResponse(chart.get_chart_image(), mimetype="image/png")


# vim: et sw=4 sts=4
