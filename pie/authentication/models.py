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
from facebook.djangofb import Facebook,get_facebook_client
from profiles.models import UserProfile

class FacebookBackend:
    
    def authenticate(self, request=None):
        fb = get_facebook_client()
        if fb.uid:
            try:
                logging.debug("Checking for user %s..." % fb.uid)
                user = User.objects.get(username=fb.uid)
            except User.DoesNotExist:
                logging.debug("User didn't exist, adding...")
                profile = UserProfile(facebook_id=fb.uid)
                logging.debug("Got profile from facebook...")
                user = User(username=fb.uid, password=self.__random_password(),email=profile.email)
                user.save()
                logging.debug("Added User account...")
                profile.user = user
                profile.save()
                logging.info("Added user and profile for %s!" % fb.uid)
            return user
        else:
            logging.debug("Invalid Facebook login for %s" % fb.__dict__)
            return None
        
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    
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
