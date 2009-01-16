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

from django.conf import settings
from django.core.management import BaseCommand
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User
from pie.profiles.models import UserProfile

class Command(BaseCommand):
    def handle(self,*args,**options):
        """this command will check for messed user accounts"""
        for user in User.objects.all():
            try:
                p = user.get_profile()
                print "User #%s OK" % user.id
            except (UserProfile.DoesNotExist):
                profile = UserProfile(user=user,facebook_id=user.username)
                profile.save()
                print "Fixed User #%s" % user.id

        
        
