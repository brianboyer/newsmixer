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

urlpatterns = patterns('',
    (r'^$', 'letters.views.index'),
    (r'^reply_to_article/(?P<article_id>\w*)$', 'letters.views.new_letter'),
    (r'^new$', 'letters.views.new_letter'),
    (r'^(?P<letter_id>\w*)/$', 'letters.views.read_letter'),
    (r'^(?P<letter_id>\w*)/reply$', 'letters.views.new_letter'),
    (r'^(?P<letter_id>\w*)/flag_as_offensive$', 'letters.views.flag_as_offensive'),
    (r'^search$', 'letters.views.search'),
    
)
