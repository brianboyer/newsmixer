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
from pie.letters.models import Letter, LetterForm

register = template.Library()
    
@register.inclusion_tag('letters/letter.html',takes_context=True)
def show_letter(context, letter):
    context.update({'letter':letter,'replies':letter.replies})
    return context
    
@register.inclusion_tag('letters/letter_simple.html',takes_context=True)
def show_simple_letter(context, letter):
    context.update({'letter':letter,'replies':letter.replies})
    return context

@register.inclusion_tag('letters/list.html',takes_context=True)
def list_letters_for_article(context, article):
    context.update({'letter_list':article.letter_set.order_by("created")})
    return context
    
@register.inclusion_tag('letters/search_box.html',takes_context=True)
def search_box(context):
    return context
