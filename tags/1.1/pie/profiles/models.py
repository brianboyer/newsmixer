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
import random
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from facebook.djangofb import Facebook,get_facebook_client
from facebook import FacebookError
from urllib2 import URLError
from pie.letters.models import Letter
from pie.bumbles.models import Bumble
from pie.questions.models import Question,Answer

FACEBOOK_FIELDS = ['uid,name,first_name,pic_square_with_logo,affiliations,status,proxied_email']
DUMMY_FACEBOOK_INFO = {
    'uid':0,
    'name':'(Private)',
    'first_name':'(Private)',
    'pic_square_with_logo':'/public/images/t_silhouette.jpg',
    'affiliations':None,
    'status':None,
    'proxied_email':None,
}

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    facebook_id = models.IntegerField(unique=True)
    following = models.ManyToManyField('self',symmetrical=False,related_name='followers',blank=True)
    __facebook_info = None
    
    def __get_picture_url(self):
        self.__configure_me()
        if self.__facebook_info['pic_square_with_logo']:
            return self.__facebook_info['pic_square_with_logo']
        else:
            return DUMMY_FACEBOOK_INFO['pic_square_with_logo']
    picture_url = property(__get_picture_url)

    def __get_profile_url(self):
        return u"http://www.facebook.com/profile.php?id=%i" % (self.facebook_id)
    profile_url = property(__get_profile_url)
    
    def __get_full_name(self):
        self.__configure_me()
        if self.__facebook_info['name']:
            return u"%s" % self.__facebook_info['name']
        else:
            return DUMMY_FACEBOOK_INFO['name']
    full_name = property(__get_full_name)
    
    def __get_first_name(self):
        self.__configure_me()
        if self.__facebook_info['first_name']:
            return u"%s" % self.__facebook_info['first_name']
        else:
            return DUMMY_FACEBOOK_INFO['first_name']
    first_name = property(__get_first_name)
    
    def __get_networks(self):
        self.__configure_me()
        return self.__facebook_info['affiliations']
    networks = property(__get_networks)
    
    def __get_status(self):
        self.__configure_me()
        if self.__facebook_info['status']:
            return self.__facebook_info['status']['message']
        else:
            return ""
    status = property(__get_status)

    def __get_email(self):
        self.__configure_me()
        if self.__facebook_info['proxied_email']:
            return self.__facebook_info['proxied_email']
        else:
            return ""
    email = property(__get_email)

    def get_friends_profiles(self,limit=50):
        '''returns primed profile objects for this persons friends'''
        friends = []
        friends_info = []
        friends_ids = []
        try:
            friends_ids = self.__get_facebook_friends()
        except (FacebookError,URLError), ex:
            logging.error("Facebook Fail getting friends: %s" % ex)
        logging.debug("Friends of %s %s" % (self.facebook_id,friends_ids))
        if len(friends_ids) > 0:
            #this will cache all the friends in one api call
            self.__get_facebook_info(friends_ids)
        for id in friends_ids:
            try:
                friends.append(UserProfile.objects.get(facebook_id=id))
            except (User.DoesNotExist, UserProfile.DoesNotExist):
                logging.error("Can't find friend profile %s" % id)
        return friends
    
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
        
    def get_activity(self):
        return {
            Bumble:self.user.bumble_set.count(),
            Letter:self.user.letter_set.count(),
            Question:self.user.question_set.count(),
            Answer:self.user.answer_set.count(),
        }

    def __get_facebook_friends(self):
        _facebook_obj = get_facebook_client()
        friends = []
        cache_key = 'fb_friends_%s' % (self.facebook_id)
    
        fb_info_cache = cache.get(cache_key)
        if fb_info_cache:
            friends = fb_info_cache
        else:
            if settings.RANDOM_FACEBOOK_FAIL and random.randint(1,10) is 8:
                raise FacebookError(102,"RANDOM FACEBOOK FAIL!!!",[])
            elif settings.RANDOM_FACEBOOK_FAIL and random.randint(1,10) is 3:
                raise URLError(104)
            logging.debug("Calling Facebook for '%s'" % cache_key)
            friends = _facebook_obj.friends.getAppUsers()
            cache.set(cache_key,friends,settings.FACEBOOK_CACHE_TIMEOUT)
        
        return friends        

    def __get_facebook_info(self,fbids):
        _facebook_obj = get_facebook_client()
        ret = []
        ids_to_get = []
        for id in fbids:
            if id is 0:
                ret.append(DUMMY_FACEBOOK_INFO)
            
            if _facebook_obj.uid is None:
                cache_key = 'fb_user_info_%s' % id
            else:
                cache_key = 'fb_user_info_%s_%s' % (_facebook_obj.uid,id)
        
            fb_info_cache = cache.get(cache_key)
            if fb_info_cache:
                ret.append(fb_info_cache)
            else:
                ids_to_get.append(id)
        
        if len(ids_to_get) > 0:
            if settings.RANDOM_FACEBOOK_FAIL and random.randint(1,10) is 8:
                raise FacebookError(102,"RANDOM FACEBOOK FAIL!!!",[])
            elif settings.RANDOM_FACEBOOK_FAIL and random.randint(1,10) is 3:
                raise URLError(104)
            logging.debug("Calling Facebook for '%s'" % ids_to_get)
            tmp_info = _facebook_obj.users.getInfo(ids_to_get, FACEBOOK_FIELDS)
            
            ret.extend(tmp_info)
            for info in tmp_info:
                if _facebook_obj.uid is None:
                    cache_key = 'fb_user_info_%s' % id
                else:
                    cache_key = 'fb_user_info_%s_%s' % (_facebook_obj.uid,info['uid'])

                cache.set(cache_key,info,settings.FACEBOOK_CACHE_TIMEOUT)
                
        return ret

    def __configure_me(self):
        try:
            logging.debug("FBID: '%s' profile: '%s' user: '%s'" % (self.facebook_id,self.id,self.user_id))
            if self.__facebook_info == DUMMY_FACEBOOK_INFO or not self.__facebook_info:
                self.__facebook_info = self.__get_facebook_info([self.facebook_id])[0]
        except (ImproperlyConfigured), ex:
            logging.error('Facebook not setup')
        except (FacebookError,URLError), ex:
            logging.error('Facebook Fail loading profile: %s' % ex)
            self.__facebook_info = DUMMY_FACEBOOK_INFO
        except (IndexError), ex:
            logging.error("Couldn't retrieve FB info for FBID: '%s' profile: '%s' user: '%s'" % (self.facebook_id,self.id,self.user_id))
            self.__facebook_info = DUMMY_FACEBOOK_INFO

    def get_absolute_url(self):
        return "/profiles/%i/" % (self.id)
    def get_follow_url(self):
        return "/profiles/%i/follow" % (self.id)
    def get_unfollow_url(self):
        return "/profiles/%i/unfollow" % (self.id)
    def __unicode__(self):
        return "Profile for %s" % self.facebook_id
