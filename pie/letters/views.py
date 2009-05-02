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

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import defaultfilters, RequestContext
from django.template.defaultfilters import truncatewords
from django.utils import simplejson

from pressroom.models import Article
from letters.models import Letter,LetterForm,EditorPick
from authentication.models import FacebookTemplate

def index(request):
    """display letters index page"""
    letter_list = [ep.letter for ep in EditorPick.objects.get_top_two_published()]
    template_dict = {
        'letter_list':letter_list,
        'all_letters':Letter.objects.all().order_by('-created'),
        'letter_count':Letter.objects.all().count,
    }
    return render_to_response('letters/index.html', template_dict, context_instance=RequestContext(request))

def read_letter(request,letter_id):
    l = Letter.objects.get(pk=letter_id)

    exclude_letters = [r for r in l.replies.all()]
    exclude_letters.append(l)
    letters = []
    if l.article:
        for let in l.article.letter_set.order_by('created'):
            if not let in exclude_letters:
                letters.append(l)

    template_dict = {
        'letter': l,
        'related_letters':letters
    }
    return render_to_response('letters/read_letter.html', template_dict, context_instance=RequestContext(request))

def search(request):
    # django-search is no more
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def new_letter(request,article_id=None,letter_id=None):    
    """add a new letter"""
    my_letter = Letter(user=request.user)
    
    #see if this is in response to an article
    try:
        a = Article.objects.get(pk=article_id)
        my_letter.article = a
    except Article.DoesNotExist:
        pass
        
    #see if this is in response to a letter
    try:
        l = Letter.objects.get(pk=letter_id)
        my_letter.article=l.article
        my_letter.letter=l
    except Letter.DoesNotExist:
        pass
    
    #this is an ajax request to create a new letter
    if request.method == "POST":
        form = LetterForm(request.POST, instance=my_letter)
        if form.is_valid():
            new_letter = form.save()
            
            #set up template data
            template_data = {
                'title': truncatewords(new_letter.title,20),
                'body':  truncatewords(new_letter.body,50),
                'url':   settings.ROOT_URL + new_letter.get_absolute_url()
            }
            if new_letter.article:
                template_data.update({
                    "headline": truncatewords(new_letter.article.headline,20),
                    "article": truncatewords(new_letter.article.body,50),
                })
            if new_letter.letter:
                template_bundle_id = FacebookTemplate.objects.get(name='letter_re_letter_re_article').template_bundle_id
                template_data.update({
                    "original_user":  new_letter.letter.user.username,
                    "original_title": truncatewords(new_letter.letter.title,20),
                    "original_body":  truncatewords(new_letter.letter.body,50),
                })
            
            #get template bundle id
            if new_letter.article:
                if new_letter.letter:
                    template_bundle_id = FacebookTemplate.objects.get(name='letter_re_letter_re_article').template_bundle_id
                else:
                    template_bundle_id = FacebookTemplate.objects.get(name='letter_re_article').template_bundle_id
            else:
                if new_letter.letter:
                    template_bundle_id = FacebookTemplate.objects.get(name='letter_re_letter').template_bundle_id
                else:
                    template_bundle_id = FacebookTemplate.objects.get(name='letter').template_bundle_id

            results = {'success':True,'template_bundle_id':template_bundle_id,'template_data':template_data}
        else:
            errors = 'Please give your letter a '
            for field in form.errors.keys():
                if field == form.errors.keys()[-1]:
                    if len(form.errors.keys()) > 1:
                        errors = errors.rstrip(', ')
                        errors += ' and %s.' % field
                    else:
                        errors += ' %s.' % field
                else:
                    errors += '%s, ' % field
            results = {'success':False,'errors':errors}
        json = simplejson.dumps(results)
        return HttpResponse(json, mimetype='application/json')
    
    #this is a request for a form to write a new letter
    else:
        form = LetterForm(instance=my_letter)
        template_dict = {
            'letter_form': form,
            'letter_template_bundle_id': FacebookTemplate.objects.get(name='letter').template_bundle_id,
            'letter_re_letter_template_bundle_id': FacebookTemplate.objects.get(name='letter_re_letter').template_bundle_id,
            'letter_re_article_template_bundle_id': FacebookTemplate.objects.get(name='letter_re_article').template_bundle_id,
            'letter_re_letter_re_article_template_bundle_id': FacebookTemplate.objects.get(name='letter_re_letter_re_article').template_bundle_id,
        }
        return render_to_response('letters/new_letter.html', template_dict, context_instance=RequestContext(request))

@login_required
def flag_as_offensive(request,letter_id):
    b = Letter.objects.get(pk=letter_id)
    b.offensive = True
    b.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
