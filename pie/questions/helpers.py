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
import random
from models import Question

def get_featured_question():
    #looks for a question from the last three days to feature
    #today is midnight today, minus two for two prev days, add one to get today
    start = datetime.date.today() - datetime.timedelta(days=2)
    end = datetime.date.today() + datetime.timedelta(days=1)
    questions = Question.objects.filter(created__range=(start,end))
    hot_question = None
    answer_me = None
    if questions.count() > 0:
        answered_questions = [q for q in questions if q.answer_set.count() > 0]
        if len(answered_questions) > 0:
            #Qs&As, we should have a hot question
            answered_questions.sort(key=lambda x:x.answer_set.count())
            hot_question = answered_questions[-1]
        else:
            #no answers, choose a random q, prompt to answer
            answer_me = questions[random.randint(0,questions.count() - 1)]
    return {'hot_question':hot_question,'answer_me':answer_me}
    
