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

from pie.letters.models import Letter,EditorPick
from django.contrib import admin

class LetterAdmin(admin.ModelAdmin):
    list_display = ('title','user','article','letter','offensive','created')
    list_filter = ('offensive',)
    search_fields = ('title',)

class EditorPickAdmin(admin.ModelAdmin):
    list_display = ('letter','pub_date')

admin.site.register(Letter,LetterAdmin)
admin.site.register(EditorPick,EditorPickAdmin)
