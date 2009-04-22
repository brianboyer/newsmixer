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

from django.db import models
from django.forms import ModelForm
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.conf import settings
import hashlib


class ServiceAccount(models.Model):
    """Manages api keys and secrets"""
    site = models.ForeignKey(Site,unique=True)
    user = models.ForeignKey(User,related_name="owner")
    api_key = models.CharField(unique=True,max_length=100)
    secret = models.CharField(max_length=100)
    
    def generate_keys(self):
        """generate api_key and secret"""
        h = hashlib.new('ripemd160')
        h.update(self.user.email+self.site.name+self.site.domain)
        self.api_key = h.hexdigest()
        h.update(settings.SECRET_KEY)
        self.secret = h.hexdigest()
    

class Article(models.Model):
    """References an article on another site"""
    service_account = models.ForeignKey(ServiceAccount)
    url = models.URLField(unique=True,verify_exists=True)
    title = models.CharField(blank=True, max_length=100)
    summary = models.TextField(blank=True)

class SiteForm(ModelForm):
    """Form for registering a new site"""
    class Meta:
        model=Site
