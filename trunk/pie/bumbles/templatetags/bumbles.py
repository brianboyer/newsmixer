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
from pie.bumbles.models import Bumble, BumbleForm
from datetime import datetime, timedelta

register = template.Library()

@register.inclusion_tag('bumbles/bumble.html', takes_context=True)
def show_bumble(context, bumble):
    context.update({'bumbles':bumbles})
    return context

@register.inclusion_tag('bumbles/bumble_form.html', takes_context=True)
def show_bumble_form(context, article=None, bumble=None, hidden=False):
    if not article:
        article = context['article']

    f = BumbleForm(instance=Bumble(user=context['user'],article=article))
    style = ''
    if hidden:
        style = 'display:none;'
    context.update({'bumble_form':f,'style':style})
    return context
    
@register.inclusion_tag('bumbles/bumbles.html', takes_context=True)
def show_article_bumbles(context, article=None):
    """Show bumbles in reverse chrono for this article"""
    if not article:
        article = context['article']
    bumbles = Bumble.objects.filter(article=article).order_by('-created')
    context.update({'bumbles':bumbles})
    return context

@register.inclusion_tag('bumbles/bumbles.html', takes_context=True)
def show_bumbles(context):
    #limit to top ten
    bumbles = Bumble.objects.all().order_by('-created')[0:10]
    context.update({'bumbles':bumbles,'show_headline':True})
    return context

@register.inclusion_tag('bumbles/bumble_script.html')
def show_bumbles_script(limit=0,show_headline='false',article=None):
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
        value = value.replace(username, "<a href=\"/bumbles/user/%s\">%s</a>" % (username.lstrip('@').lower(), username))
    return mark_safe(value)
