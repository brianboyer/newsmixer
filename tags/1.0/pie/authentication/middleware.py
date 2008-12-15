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
from datetime import datetime
from django.contrib.auth import logout
from django.conf import settings
from facebook import Facebook,FacebookError
from django.template import TemplateSyntaxError
from django.http import HttpResponseRedirect,HttpResponse
from urllib2 import URLError

class FacebookConnectMiddleware(object):
    """Middlware to provide a working facebook object"""
    def process_request(self,request):
        """process incoming request"""
        try:
            request.profile = None
            if request.user.is_authenticated():
                bona_fide = request.facebook.check_session(request)
                request.profile = request.user.get_profile()
                if not bona_fide and not request.user.is_superuser:
                    logout(request)
        except Exception, ex:
            #Because this is a middleware, we can't assume the errors will be caught elsewhere.
            warnings.warn(u'FBC Middleware failed: ' + unicode(ex))
            logging.exception('FBC Middleware: something went terribly wrong')        
   
# this doesnt really do much anymore
# prob can kill it?
# keep around to make debugging easier?
# the FailMiddleware deals with errors now
   
#    def process_exception(self,request,exception):
#        my_ex = exception
#        if type(exception) == TemplateSyntaxError:
#            if getattr(exception,'exc_info',False):
#                my_ex = exception.exc_info[1]

#        if type(my_ex) == FacebookError:
#            if getattr(my_ex,'code',None) == 102:
#                logging.exception('FBC Middleware: 102, session')
#            else:
#                logging.exception('FBC Middleware: ???, unknown')
#        elif type(my_ex) == URLError:
#            if getattr(my_ex,'code',None) == 104:
#                logging.exception('FBC Middleware: 104, connection reset?')
#            elif getattr(my_ex,'code',None) == -2:
#                logging.exception('FBC Middleware: 102, name or service not known')
#        else:
#            logging.exception('FBC Middleware: oh, the horror')
