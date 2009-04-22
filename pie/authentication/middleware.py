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

import logging
import warnings
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.conf import settings
from facebook import Facebook,FacebookError
from django.template import TemplateSyntaxError
from django.http import HttpResponseRedirect,HttpResponse
from urllib2 import URLError
from profiles.models import UserProfile

class FacebookConnectMiddleware(object):
    """Middlware to provide a working facebook object"""
    def process_request(self,request):
        """process incoming request"""
        try:
            bona_fide = request.facebook.check_session(request)
            if request.user.is_authenticated() and request.user.get_profile().facebook_only():
                cur_user = request.facebook.users.getLoggedInUser()
                logging.debug("Bona Fide: %s Logged in: %s FB Obj: %s" % (bona_fide,cur_user,request.facebook.uid))
                if not bona_fide or int(cur_user) != int(request.facebook.uid):
                    logging.debug("DIE DIE DIE")
                    logout(request)
                    request.facebook.session_key = None
                    request.facebook.uid = None
        except UserProfile.DoesNotExist, ex:
            #This user is not from facebook so they are ok
            pass
        except Exception, ex:
            #Because this is a middleware, we can't assume the errors will be caught elsewhere.
            logout(request)
            request.facebook.session_key = None
            request.facebook.uid = None
            warnings.warn(u'FBC Middleware failed: %s' % ex)
            logging.exception('FBC Middleware: something went terribly wrong')
   
    def process_exception(self,request,exception):
        my_ex = exception
        if type(exception) == TemplateSyntaxError:
            if getattr(exception,'exc_info',False):
                my_ex = exception.exc_info[1]

        if type(my_ex) == FacebookError:
            if my_ex.code is 102:
                logout(request)
                request.facebook.session_key = None
                request.facebook.uid = None
                logging.error('FBC Middleware: 102, session')
                return HttpResponseRedirect(reverse('authentication.views.facebook_login'))
        elif type(my_ex) == URLError:
            if my_ex.reason is 104:
                logging.error('FBC Middleware: 104, connection reset?')
            elif my_ex.reason is 102:
                logging.error('FBC Middleware: 102, name or service not known')
