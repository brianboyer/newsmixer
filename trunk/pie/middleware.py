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
from django.contrib.auth import logout
from django.shortcuts import render_to_response

class FailMiddleware(object):
    """Middlware to clean up when the fit hits the shan"""
    
    def process_exception(self,request,exception):
        try:
            warnings.warn('Fail. ' + unicode(exception))
            logging.exception('Fail.')
            #logout flushes session and removes user from the request object
            logout(request)
            request.facebook.session_key = None
            request.facebook.uid = None
            #return render_to_response('500.html')
        except Exception, ex:
            warnings.warn(u'FailMiddleware, ironically, failed: ' + unicode(ex))
            logging.exception('FailMiddleware, ironically, failed')
