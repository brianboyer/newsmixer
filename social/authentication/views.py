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

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout

def facebook_login(request):
    if request.method == "POST":
        next = request.POST['next']
        user = authenticate(request=request)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect(next)
            else:
                raise FacebookAuthError('This account is disabled.')
        else:
            raise FacebookAuthError('Invalid login.')
    else:
        #login_required decorator sent us here
        return render_to_response(
            'accounts/login.html',
            {'hide_primary_login': True,},
            context_instance=RequestContext(request),
        )

def facebook_logout(request):
    logout(request)
    request.facebook.session_key = None
    request.facebook.uid = None
    return HttpResponse('Logged out!')
    #return HttpResponseRedirect('/')
    
class FacebookAuthError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

