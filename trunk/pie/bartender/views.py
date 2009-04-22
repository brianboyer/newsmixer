# Copyright 2009 Ryan Mark
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

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.http import HttpResponseRedirect,HttpResponse,HttpResponseServerError
from django import template
import logging
from jsmin import jsmin
from jspacker import JavaScriptPacker

from bartender.models import ServiceAccount, Article, SiteForm
from quips.models import QuipForm

@login_required
def dashboard(request):
    """dashboard for a newsmixer service (bartender) account"""
    template_dict = {
        "service_account": ServiceAccount.objects.filter(user=request.user),
    }
    return render_to_response('bartender/dashboard.html', template_dict, context_instance=RequestContext(request))
    
@login_required
def signup(request):
    """signup a new site for the newsmixer service"""
    
    if request.method == "POST":
        form = SiteForm(request.POST)
        if form.is_valid():
            new_site = form.save()
            my_service_account = ServiceAccount(user=request.user,site=new_site)
            my_service_account.generate_keys()
            my_service_account.save()
            return HttpResponseRedirect(reverse("bartender.views.dashboard"))

    template_dict = {
        "form": SiteForm(),
    }
    return render_to_response('bartender/signup.html', template_dict, context_instance=RequestContext(request))
    
def embed(request,api_key):
    """get the embeddable javascript"""
    
    if request.method == "GET":
        try:
            my_service_account = ServiceAccount.objects.get(api_key=api_key)
        except ServiceAccount.DoesNotExist,ex:
            return HttpResponseServerError("Not allowed")

        context = RequestContext(request)
        p = JavaScriptPacker()
        context.update({"sa":my_service_account,"quip_form":QuipForm()})
    
        t = template.loader.get_template('bartender/embed.js')
        i = t.render(context)
        #i = p.pack(t.render(context),compaction=True, encoding=62, fastDecode=True)
    
        return HttpResponse(i, mimetype='text/javascript')