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

import unittest
from django.contrib.auth.models import User
from authentication.models import FacebookBackend
from profiles.models import UserProfile
    
class FacebookBackendTestCase(unittest.TestCase):
    
    def setUp(self):
        self.test_user = User.objects.create(username='4321', password='test')
        
    def tearDown(self):
        self.test_user.delete()
    
    def test_get_user(self):
        fbb = FacebookBackend()
        
        #user does not exist
        user = fbb.get_user(1234)
        self.assertEqual(user, None)
        
        #user exists
        user = fbb.get_user(self.test_user.id)
        self.assertEqual(user, self.test_user)
        
    def test_random_password(self):
        fbb = FacebookBackend()
        password = fbb._FacebookBackend__random_password()
        self.assertEqual(len(password), 8)

    def test_get_or_create_user(self):
        fbb = FacebookBackend()
        
        #user exists
        facebook_info = {
            'uid':        self.test_user.username,
            'proxied_email': 'dna@douglasadams.com',
        }
        user = fbb._FacebookBackend__get_or_create_user(facebook_info)
        self.assertEqual(user, self.test_user)
        
        #user does not exist and must be created
        #does it return the new user
        facebook_info = {
            'uid':           '666',
            'proxied_email': 'dna@douglasadams.com',
        }
        user = fbb._FacebookBackend__get_or_create_user(facebook_info)
        self.assertEqual(user.username, facebook_info['uid'])
        self.assertEqual(user.email, facebook_info['proxied_email'])
        self.assertEqual(str(user.get_profile().facebook_id), facebook_info['uid'])
        #did it create the user in the database correctly?
        user = User.objects.get(username=facebook_info['uid'])
        self.assertEqual(user.username, facebook_info['uid'])
        self.assertEqual(user.email, facebook_info['proxied_email'])
        self.assertEqual(str(user.get_profile().facebook_id), facebook_info['uid'])
