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

import datetime
import logging
from django.shortcuts import render_to_response
from django.template import RequestContext

from bartender.models import Article
from quips.models import Quip
from questions.models import Answer, Question
from questions.helpers import get_featured_question
from letters.models import Letter, EditorPick
from profiles.helpers import get_top_recent_comment

def index(request):
    articles_and_picks = []
    articles_and_picks.extend(Article.objects.get_published())
    articles_and_picks.extend(EditorPick.objects.get_published())
    articles_and_picks.sort(key=lambda x: x.pub_date)
    articles_and_picks.reverse()
    articles_and_picks = articles_and_picks[:8]
    
    featured_question = get_featured_question()
    featured_comment = None
    if request.user.is_authenticated() and request.user.get_profile():
        featured_comment = get_top_recent_comment(request.user.get_profile().get_friends_profiles())
  
    return render_to_response(
        "index.html",
        {
            'hide_primary_login': True,
            'articles_and_picks': articles_and_picks,
            'featured_question':  featured_question,
            'featured_comment':   featured_comment,
        },
        context_instance=RequestContext(request)
    )