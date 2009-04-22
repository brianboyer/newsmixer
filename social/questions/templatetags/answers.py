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

from django import template
from questions.models import QuestionForm
from django.utils import simplejson

register = template.Library()
    
@register.inclusion_tag('questions/answer.html', takes_context=True)
def show_answer(context, answer):
    context.update({'answer':answer,})
    return context

@register.inclusion_tag('questions/questions_script.html',takes_context=True)
def show_questions_script(context,article=None):
    context.update({
        'question_form': QuestionForm(),
    })
    if article:
        context['article'] = article
    annotations = context['article'].question_set.order_by('block','-created')
    annotation_info = {}
    for a in annotations:
        if not a.block in annotation_info.keys():
            annotation_info[a.block] = {'questions':0,'answers':0}
        annotation_info[a.block]['questions'] += 1
        annotation_info[a.block]['answers'] += a.answer_set.count()
    context['annotation_info_js'] = simplejson.dumps(annotation_info)
    return context

        
