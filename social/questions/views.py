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
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template.defaultfilters import truncatewords
from django.template import Context, RequestContext
from django.utils import simplejson

from bartender.models import Article
from questions.models import *
from authentication.models import FacebookTemplate

def get_questions(request):
    if request.method == "POST":
        a = Article.objects.get(pk=request.POST['article'])
        questions = a.question_set.filter(block=request.POST['block']).order_by('-created')
        template_dict = {
            'questions': questions,
            'answer_form': AnswerForm(),
        }
        if questions.count() > 0:
            template_dict['next']=questions[0].get_absolute_url()
        return render_to_response('questions/ajax_article_questions.html', template_dict, context_instance=RequestContext(request))

@login_required
def add_answer(request,object_id):
    q = Question.objects.get(pk=object_id)
    
    if request.method == "POST":
        f = AnswerForm(request.POST, instance=Answer(user=request.user,question=q))
        if f.is_valid():
            f.save()
            template_bundle_id = FacebookTemplate.objects.get(name='answer').template_bundle_id
            template_data = {
                "asker":       f.instance.question.user.username,
                "question":    f.instance.question.text,
                "answer":      f.instance.text,
                "url":         settings.ROOT_URL + f.instance.get_absolute_url(),
                "headline":    truncatewords(f.instance.question.article.headline,20),
                "article":     truncatewords(f.instance.question.article.body,50)
            }
            results = {
                'success':True,
                'block':q.block,
                'answer_id':f.instance.id,
                'template_bundle_id':template_bundle_id,
                'template_data':template_data,
            }
        else:
            errors = ''
            if 'text' in f.errors.keys():
                errors += 'Please type an answer.'
            if 'reference' in f.errors.keys():
                errors += ' Please enter a url. (eg. http://en.wikipedia.org/wiki/Donuts)'
            if errors == '':
                errors = ' There was a problem. Sorry.'
            results = {'success':False,'errors':errors}
        json = simplejson.dumps(results)
        return HttpResponse(json, mimetype='application/json')
    else:
        raise Http404
        
@login_required
def add_question(request,object_id,block_id=-1):
    a = Article.objects.get(pk=object_id)
    
    if request.method == "POST":
        if block_id >= 0:
            f = QuestionForm(request.POST, instance=Question(user=request.user,article=a,block=block_id))
        else:
            f = QuestionForm(request.POST, instance=Question(user=request.user,article=a))
        
        if f.is_valid():
            f.save()
            template_data = {
                "question": truncatewords(f.instance.text,50),
                "url":      settings.ROOT_URL + f.instance.get_absolute_url(),
                "headline": truncatewords(f.instance.article.headline,20),
                "article":  truncatewords(f.instance.article.body,50),
            }
            template_bundle_id = FacebookTemplate.objects.get(name='question').template_bundle_id
            results = {
                'success':True,
                'block':block_id,
                'question_id':f.instance.id,
                'template_bundle_id':template_bundle_id,
                'template_data':template_data,
            }
        else:
            errors = ''
            if 'text' in f.errors.keys():
                errors = 'Please type a question.'
            else:
                errors = 'There was a problem. Sorry.'
            results = {'success':False,'errors':errors}
            
        json = simplejson.dumps(results)
        return HttpResponse(json, mimetype='application/json')  
    else:
        raise Http404

@login_required
def flag_question_as_offensive(request,question_id):
    """set the offensive flag on a question"""
    q = Question.objects.get(pk=question_id)
    q.offensive=True
    q.save()
    return HttpResponseRedirect('/articles/'+str(q.article.id))
