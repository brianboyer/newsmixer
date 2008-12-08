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

from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
from django.views.generic.simple import direct_to_template
from django.conf import settings
from pressroom.models import Article

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'bumbles.views.get_bumbles'),
    (r'^create$', 'bumbles.views.create'),
    (r'^create/(?P<option>\w+)$', 'bumbles.views.create'),
    (r'^flag_as_offensive/(?P<bumble_id>\d+)/$', 'bumbles.views.flag_as_offensive'),
)
