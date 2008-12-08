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

import sha, random
import logging
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from facebook import Facebook
from profiles.models import UserProfile

class FacebookBackend:
    
    def authenticate(self, request=None):
        fb = Facebook(settings.FACEBOOK_API_KEY, settings.FACEBOOK_SECRET_KEY)
        fb.check_session(request)
        if fb.uid:
            facebook_info = fb.users.getInfo([fb.uid], ['uid', 'proxied_email'])[0]
            my_user = self.__get_or_create_user(facebook_info)
            return my_user
        else:
            return None
        
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def __get_or_create_user(self, facebook_info):
        try:
            user = User.objects.get(username=facebook_info['uid'])
        except User.DoesNotExist:
            #TODO: need a transaction here
            user = User(username=facebook_info['uid'], password=self.__random_password())
            user.email = facebook_info['proxied_email']
            user.save()
            profile = UserProfile(user=user,facebook_id=facebook_info['uid'])
            profile.save()
        return user
    
    def __random_password(self):
        return sha.new(str(random.random())).hexdigest()[:8]
        
class BigIntegerField(models.IntegerField):
	empty_strings_allowed=False
	def get_internal_type(self):
		return "BigIntegerField"
	
	def db_type(self):
		return 'NUMBER(19)' if settings.DATABASE_ENGINE == 'oracle' else 'bigint'


class FacebookTemplate(models.Model):
    name = models.SlugField(unique=True)
    template_bundle_id = BigIntegerField()
    
    def __unicode__(self):
        return self.name.capitalize()
