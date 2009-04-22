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

from django.contrib.auth.models import User
from django import template
from pie.quips.models import Quip, QuipForm
from datetime import datetime, timedelta

register = template.Library()

@register.inclusion_tag('quips/quip.html', takes_context=True)
def show_quip(context, quip):
    context.update({'quips':quips})
    return context

@register.inclusion_tag('quips/quip_form.html', takes_context=True)
def show_quip_form(context, article=None, quip=None, hidden=False):
    if not article:
        article = context['article']

    f = QuipForm(instance=Quip(user=context['user'],article=article))
    style = ''
    if hidden:
        style = 'display:none;'
    context.update({'quip_form':f,'style':style})
    return context
    
@register.inclusion_tag('quips/quips.html', takes_context=True)
def show_article_quips(context, article=None):
    """Show quips in reverse chrono for this article"""
    if not article:
        article = context['article']
    quips = Quip.objects.filter(article=article).order_by('-created')
    context.update({'quips':quips})
    return context

@register.inclusion_tag('quips/quips.html', takes_context=True)
def show_quips(context):
    #limit to top ten
    quips = Quip.objects.all().order_by('-created')[0:10]
    context.update({'quips':quips,'show_headline':True})
    return context

@register.inclusion_tag('quips/quip_script.html')
def show_quips_script(limit=0,show_headline='false',article=None):
    if article != None:
        artid=article.id
    else:
        artid=0
    return {'limit':limit,'show_headline':show_headline,'article':artid}
    
from django.utils.safestring import mark_safe

@register.filter
def link_user(value):
    usernames = [word for word in value.split(' ') if word.startswith('@')]
    for username in usernames:
        value = value.replace(username, "<a href=\"/quips/user/%s\">%s</a>" % (username.lstrip('@').lower(), username))
    return mark_safe(value)
