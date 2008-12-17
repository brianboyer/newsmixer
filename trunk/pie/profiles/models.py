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
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from facebook.djangofb import Facebook,get_facebook_client
from facebook import FacebookError
from pie.letters.models import Letter
from pie.bumbles.models import Bumble
from pie.questions.models import Question,Answer

FACEBOOK_FIELDS = ['uid,name,first_name,pic_square_with_logo,affiliations,status']

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    facebook_id = models.IntegerField()
    following = models.ManyToManyField('self',symmetrical=False,related_name='followers',blank=True)
    __facebook_info = None
    __facebook_obj = None
    __friends_profiles = None
    
    def __get_picture_url(self):
        return self.__facebook_info['pic_square_with_logo']
    picture_url = property(__get_picture_url)

    def __get_profile_url(self):
        return u"http://www.facebook.com/profile.php?id=%i" % (self.facebook_id)
    profile_url = property(__get_profile_url)
    
    def __get_full_name(self):
        return u"%s" % self.__facebook_info['name']
    full_name = property(__get_full_name)
    
    def __get_first_name(self):
        return u"%s" % self.__facebook_info['first_name']
    first_name = property(__get_first_name)
    
    def __get_networks(self):
        return self.__facebook_info['affiliations']
    networks = property(__get_networks)
    
    def __get_status(self):
        if self.__facebook_info['status']:
            return self.__facebook_info['status']['message']
        else:
            return ""
    status = property(__get_status)
    
    def get_friends_profiles(self):
        '''returns primed profile objects for this persons friends'''
        if not self.__friends_profiles:
            friends = []
            friends_info = []
            friend_ids = self.__facebook_obj.friends.getAppUsers()
            if len(friend_ids) > 0:
                friends_info = self.__facebook_obj.users.getInfo(friend_ids,FACEBOOK_FIELDS)
            for f in friends_info:
                cache.add('fb_user_info_%s_%s' % (self.__facebook_obj.uid,f['uid']), f,3600)
                try:
                    cur_profile = UserProfile.objects.get(user=User.objects.get(username=f['uid']))
                    friends.append(cur_profile)
                except (User.DoesNotExist, UserProfile.DoesNotExist):
                    pass
            self.__friends_profiles = friends
        return self.__friends_profiles
    
    def get_following_profiles(self):
        '''returns primed profile objects for the folks this person follows'''
        #should run a getinfo and prime the cache before the next line
        return self.following.all()
    
    def get_followers_profiles(self):
        '''returns primed profile objects for the folks who follow this person'''
        #should run a getinfo and prime the cache before the next line
        return self.followers.all()

    def get_recent_comments(self):
        my_stuff = []
        my_stuff.extend(self.user.letter_set.all())
        my_stuff.extend(self.user.bumble_set.all())
        my_stuff.extend(self.user.question_set.all())
        my_stuff.extend(self.user.answer_set.all())
        my_stuff.sort(key=lambda x: x.created)
        my_stuff.reverse()
        return my_stuff        

    def __init__(self, *args, **kwargs):
        super(UserProfile, self).__init__(*args, **kwargs)
        try:
            self.__facebook_obj = get_facebook_client()
            if self.__facebook_obj.uid is None:
                fb_info_cache = cache.get('fb_user_info_%s' % self.facebook_id)
                if fb_info_cache:
                    self.__facebook_info = fb_info_cache
                else:
                    self.__facebook_info = self.__facebook_obj.users.getInfo([self.facebook_id], FACEBOOK_FIELDS)[0]
                    cache.set('fb_user_info_%s' % self.facebook_id,self.__facebook_info,3600)
            else:
                fb_info_cache = cache.get('fb_user_info_%s_%s' % (self.__facebook_obj.uid,self.facebook_id))
                if fb_info_cache:
                    self.__facebook_info = fb_info_cache
                else:
                    self.__facebook_info = self.__facebook_obj.users.getInfo([self.facebook_id], FACEBOOK_FIELDS)[0]
                    cache.set('fb_user_info_%s_%s' % (self.__facebook_obj.uid,self.facebook_id),self.__facebook_info,3600)
       
        except (ImproperlyConfigured), ex:
            logging.warn(ex)

    def setup_facebook(self,fb_obj=None,fb_info=None):
        pass
        
    def get_activity(self):
        return {
            Bumble:self.user.bumble_set.count(),
            Letter:self.user.letter_set.count(),
            Question:self.user.question_set.count(),
            Answer:self.user.answer_set.count(),
        }

    def get_absolute_url(self):
        return "/profiles/%i/" % (self.id)
    def get_follow_url(self):
        return "/profiles/%i/follow" % (self.id)
    def get_unfollow_url(self):
        return "/profiles/%i/unfollow" % (self.id)
    def __unicode__(self):
        return "Facebook user %s" % self.full_name
