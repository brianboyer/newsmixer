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
import unittest

from bartender.models import Article
from django.contrib.auth.models import User

from questions.helpers import get_featured_question
from questions.models import Question, Answer

class HelpersTestCase(unittest.TestCase):
    
    def setUp(self):
        self.test_user = User.objects.create(username='4321', password='test')
        self.test_article = Article.objects.create(headline='headline',body='body')
        
        #out of range question, five days ago
        five_days_ago = datetime.datetime.today() - datetime.timedelta(days=5)
        self.test_question = Question.objects.create(text='five days ago',user=self.test_user,article=self.test_article)
        self.test_question.created = five_days_ago
        self.test_question.save()
       
    def test_get_featured_question(self):

        #no questions in range
        fq = get_featured_question()
        self.assertEqual(None, fq['hot_question'])
        self.assertEqual(None, fq['answer_me'])
        
        #no answered question, so prompting for an answer
        unanswered_question = Question.objects.create(text='boring question',user=self.test_user,article=self.test_article)
        fq = get_featured_question()
        self.assertEqual(None, fq['hot_question'])
        self.assertEqual(unanswered_question, fq['answer_me'])
        
        #an answered question!  we have a hot one!
        hot_question = Question.objects.create(text='exciting question',user=self.test_user,article=self.test_article)
        Answer.objects.create(text='answer to exciting question',question=hot_question,user=self.test_user)
        fq = get_featured_question()
        self.assertEqual(hot_question, fq['hot_question'])
        self.assertEqual(None, fq['answer_me'])
        
        #a question with more answers, hotter stuff
        hotter_question = Question.objects.create(text='hotter question today',user=self.test_user,article=self.test_article)
        Answer.objects.create(text='hotter answer one',question=hotter_question,user=self.test_user)
        Answer.objects.create(text='hotter answer two',question=hotter_question,user=self.test_user)
        fq = get_featured_question()
        self.assertEqual(hotter_question, fq['hot_question'])
        self.assertEqual(None, fq['answer_me'])
        
    def tearDown(self):
        pass
