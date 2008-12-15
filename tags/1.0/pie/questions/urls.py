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
    (r'^$', 'questions.views.get_questions'),
    (r'^(?P<object_id>\d+)/answer$', 'questions.views.add_answer'),
    (r'^add_to_article/(?P<object_id>\d+)/?$', 'questions.views.add_question'),
    (r'^add_to_article/(?P<object_id>\d+)/(?P<block_id>\d+)/$', 'questions.views.add_question'),
    (r'^flag_question/(?P<question_id>\d+)/$', 'questions.views.flag_question_as_offensive'),
)
