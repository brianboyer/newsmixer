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

from django.template import defaultfilters
from django.utils.safestring import mark_safe

from pressroom.models import Article
from quips.models import Quip
from questions.models import Answer, Question
from letters.models import Letter

def get_comments(profiles):
    comments = []
    for p in profiles:
        comments.extend(p.get_recent_comments())
    return comments

def get_top_recent_comment(profiles):
    friend = None
    quip = None
    question = None
    answer = None
    letter = None
    activity = {Quip:0,Question:0,Answer:0,Letter:0}

    comments = get_comments(profiles)
   
    #limit to last week
    comments = [c for c in comments if c.created.date() > datetime.date.today() - datetime.timedelta(days=6)]
    
    #construct a message
    if len(comments) > 0:
        comments.sort(key=lambda x: x.created)
        comment = comments[-1]
        friend = comment.user.get_profile()
        if isinstance(comment,Quip):
            quip = comment
        elif isinstance(comment,Answer):
            answer = comment
        elif isinstance(comment,Question):
            question = comment
        elif isinstance(comment,Letter):
            letter = comment
        for c in comments:
            activity[type(c)] += 1 
                
    return {
        'friend':   friend,
        'quip':   quip,
        'question': question,
        'answer':   answer,
        'letter':   letter,
        'activity': activity
    }
