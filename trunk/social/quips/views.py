# Copyright 2008 Brian Boyer, Ryan Mark, Angela Nitzke, Joshua Pollock,
# Stuart Tiffen, Kayla Webley and the Medill School of Journalism, Northwestern
# University.
#
# This file is part of Crunchberry Pie.
#
# Crunchberry Pie is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Crunchberry Pie is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with Crunchberry Pie.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404,HttpResponseServerError
from django.shortcuts import render_to_response
from django import template
from django.template import Context, RequestContext
from django.template.defaultfilters import truncatewords
from django.utils import simplejson
from django.core import serializers

from bartender.models import Article
from quips.models import Quip, QuipForm
from facebook import Facebook
from facebookconnect.models import FacebookTemplate

import logging

def get_quips(request):
    """ajax request for more quips"""
    if request.method == "POST":
        i = None;
        if request.POST.get('article_url',False):
            recent_quips = Quip.objects.filter(created__gt=request.POST['since'],article=Article.objects.get(url=request.POST['article_url'])).order_by('-created')
        else:
            recent_quips = Quip.objects.filter(created__gt=request.POST['since']).order_by('-created')
        if recent_quips:
            context = RequestContext(request)
            if request.POST['show_headline'] == 'true':
                hedline = True
            else:
                hedline = False
            context.update({'quips':recent_quips,'show_headline':hedline})
            t = template.loader.get_template('quips/quip_list.html')
            i = t.render(context)
        json = simplejson.dumps({
            'date':datetime.now().isoformat(' '),
            'insert':i,
            'quips':recent_quips.count(),
        })
        return HttpResponse(json, mimetype='application/json')

VERB_COLORS = {
    'thinks':    '#079107',
    'loves':     '#611739',
    'feels':     '#9d6884',
    'agrees':    '#cb8337',
    'disagrees': '#6b6b6d',
    'wonders':   '#2a436a',
    'hates':     '#2e2a2b',
    }

#@login_required
def create(request,option=None):
    if request.method == "POST":
        f = QuipForm(request.POST, instance=Quip(user=request.user))
        if f.is_valid():
            new_quip = f.save()
            verb = f.instance.verb
            template_data = {
                "verb":        verb,
                "verb_color":  VERB_COLORS[verb],
                "quip":      f.instance.message,
                "url":         settings.ROOT_URL + f.instance.get_absolute_url(),
                "headline":    truncatewords(f.instance.article.headline,20),
                "article":     truncatewords(f.instance.article.body,50),
            }
            template_bundle_id = FacebookTemplate.objects.get(name='quip').template_bundle_id
            results = {
                'success':True,
                'date':datetime.now().isoformat(' '),
                'template_bundle_id':template_bundle_id,
                'template_data':template_data
            }
        else:
            if 'message' in f.errors.keys():
                errors = 'Please type a message.'
            else:
                errors = 'There was a problem.  Sorry.'
            results = {'success':False,'errors':errors}
        json = simplejson.dumps(results)
        if option:
            return HttpResponse(json, mimetype='application/json')            
        else:
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        
    else:
        raise Http404

@login_required
def flag_as_offensive(request,quip_id):
    if request.method == "POST":
        b = Quip.objects.get(pk=quip_id)
        b.offensive = True
        b.save()
        return HttpResponseRedirect(b.get_absolute_url())
    else:
        raise Http404
    
def api_get(request):
    form_url = getattr(request.GET,'form_url','')
    try:
        article = Article.objects.get(slug=request.GET['url'])
    except Article.DoesNotExist:
        article = Article(slug=request.GET['url'], headline=request.GET['headline'])
        article.save()
        
    context = RequestContext(request)

    context.update({
        'quips': Quip.objects.filter(article=article).order_by('-created'),
        'quip_form': QuipForm(instance=Quip(user=context['user'],article=article)),
        'style':'',
        'url':form_url,
    })
    
    t = template.loader.get_template('quips/quips.html')
    i = t.render(context)
    
    t = template.loader.get_template('quips/quip_form.html')
    f = t.render(context)
    
    json = simplejson.dumps({
        'insert':i,
        'form':f
    })
    return HttpResponse(json, mimetype='application/json')