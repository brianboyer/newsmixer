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

from bartender.models import Article
from quips.models import Quip
from questions.models import Answer, Question
from letters.models import Letter

from profiles.models import UserProfile
from profiles.helpers import get_top_recent_comment

class HelpersTestCase(unittest.TestCase):
    
    def setUp(self):
        
        #enemy and friends
        self.test_enemy = User.objects.create(username='1234', password='test')
        ep = UserProfile.objects.create(user=self.test_enemy,facebook_id=1234)
        self.test_friend_one = User.objects.create(username='4321', password='test')
        f1p = UserProfile.objects.create(user=self.test_friend_one,facebook_id=4321)
        self.test_friend_two = User.objects.create(username='2341', password='test')
        f2p = UserProfile.objects.create(user=self.test_friend_two,facebook_id=2341)
        self.test_friends = [f1p,f2p]
        
        self.test_article = Article.objects.create(headline='headline',body='body')
        
        #question by a friend, ten days ago
        ten_days_ago = datetime.datetime.today() - datetime.timedelta(days=10)
        q = Question.objects.create(text='ten days ago',user=self.test_friend_one,article=self.test_article)
        q.created = ten_days_ago
        q.save()
       
        #quip by an enemy, recent
        b = Quip.objects.create(message='if i hate you',verb='wonders',user=self.test_enemy,article=self.test_article)
       
    def mock_activity(self,b=0,q=0,a=0,l=0):
        return {Quip:b,Question:q,Answer:a,Letter:l}
       
    def test_get_top_recent_comment(self):

        #nothing by friends in range
        tc = get_top_recent_comment(self.test_friends)
        self.assertEqual(None, tc['friend'])
        self.assertEqual(None, tc['quip'])
        self.assertEqual(None, tc['question'])
        self.assertEqual(None, tc['answer'])
        self.assertEqual(None, tc['letter'])
        self.assertEqual(self.mock_activity(), tc['activity'])
        
        #first quip
        b1 = Quip.objects.create(message='this is great',verb='thinks',user=self.test_friend_one,article=self.test_article)
        tc = get_top_recent_comment(self.test_friends)
        self.assertEqual(self.test_friend_one.get_profile(), tc['friend'])
        self.assertEqual(b1  , tc['quip'])
        self.assertEqual(None, tc['question'])
        self.assertEqual(None, tc['answer'])
        self.assertEqual(None, tc['letter'])
        self.assertEqual(self.mock_activity(1), tc['activity'])
        
        #second, more recent quip
        b2 = Quip.objects.create(message='this is also great',verb='thinks',user=self.test_friend_two,article=self.test_article)
        tc = get_top_recent_comment(self.test_friends)
        self.assertEqual(self.test_friend_two.get_profile(), tc['friend'])
        self.assertEqual(b2,   tc['quip'])
        self.assertEqual(None, tc['question'])
        self.assertEqual(None, tc['answer'])
        self.assertEqual(None, tc['letter'])
        self.assertEqual(self.mock_activity(2), tc['activity'])
        
        #toss in a question
        q1 = Question.objects.create(text="i dont understand",user=self.test_friend_one,article=self.test_article)
        tc = get_top_recent_comment(self.test_friends)
        self.assertEqual(self.test_friend_one.get_profile(), tc['friend'])
        self.assertEqual(None, tc['quip'])
        self.assertEqual(q1,   tc['question'])
        self.assertEqual(None, tc['answer'])
        self.assertEqual(None, tc['letter'])
        self.assertEqual(self.mock_activity(2,1), tc['activity'])        

        #toss in another question
        q2 = Question.objects.create(text="i still dont understand",user=self.test_friend_one,article=self.test_article)
        tc = get_top_recent_comment(self.test_friends)
        self.assertEqual(self.test_friend_one.get_profile(), tc['friend'])
        self.assertEqual(None, tc['quip'])
        self.assertEqual(q2,   tc['question'])
        self.assertEqual(None, tc['answer'])
        self.assertEqual(None, tc['letter'])
        self.assertEqual(self.mock_activity(2,2), tc['activity'])
        
        #answer a question
        a1 = Answer.objects.create(text="it's quite simple, really'",user=self.test_friend_two,question=q1)
        tc = get_top_recent_comment(self.test_friends)
        self.assertEqual(self.test_friend_two.get_profile(), tc['friend'])
        self.assertEqual(None, tc['quip'])
        self.assertEqual(None, tc['question'])
        self.assertEqual(a1  , tc['answer'])
        self.assertEqual(None, tc['letter'])
        self.assertEqual(self.mock_activity(2,2,1), tc['activity'])
        
        #answer another question
        a2 = Answer.objects.create(text="it's still quite simple, really'",user=self.test_friend_two,question=q1)
        tc = get_top_recent_comment(self.test_friends)
        self.assertEqual(self.test_friend_two.get_profile(), tc['friend'])
        self.assertEqual(None, tc['quip'])
        self.assertEqual(None, tc['question'])
        self.assertEqual(a2  , tc['answer'])
        self.assertEqual(None, tc['letter'])
        self.assertEqual(self.mock_activity(2,2,2), tc['activity'])
        
        #write a letter to the editor        
        l1 = Letter.objects.create(title="I'm sick and tired.",body='I think that all right-thinking people in this country',user=self.test_friend_one)
        tc = get_top_recent_comment(self.test_friends)
        self.assertEqual(self.test_friend_one.get_profile(), tc['friend'])
        self.assertEqual(None, tc['quip'])
        self.assertEqual(None, tc['question'])
        self.assertEqual(None, tc['answer'])
        self.assertEqual(l1,   tc['letter'])
        self.assertEqual(self.mock_activity(2,2,2,1), tc['activity'])
        
    def tearDown(self):
        pass
