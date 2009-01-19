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

from settings_global import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG
ADMINS = (
    ('Your Name', 'yourname@example.com'),
)
DEFAULT_FROM_EMAIL = "website@example.com"
MANAGERS = ADMINS

ROOT_URL = 'http://example.com'
PIE_ROOT = '/var/www/pie'
STATIC_DOC_ROOT = PIE_ROOT + '/public'
MEDIA_ROOT = PIE_ROOT + '/public/'
TEMPLATE_DIRS = (
    PIE_ROOT + '/templates',
)

# Logging helps debugging
#import logging
#logging.basicConfig(
#    level = logging.INFO,
#    format = '%(asctime)s %(levelname)s %(message)s',
#    filename = PIE_ROOT + '/newsmixer.log',
#    filemode = 'a'
#)

DATABASE_ENGINE = ''           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Replace with keys from Facebook
FACEBOOK_API_KEY = '00000000000000000000000000000000'
FACEBOOK_SECRET_KEY = '00000000000000000000000000000000'
FACEBOOK_INTERNAL = False

# Make this unique, and don't share it with anybody.
SECRET_KEY = '00000000000000000000000000000000000000000000000000'

# Please setup caching
#CACHE_BACKEND = 'db://newsmixer_cache'

# If you're using Pie as a backend for widgets, turn this on. Little things will change
#WIDGET_MODE = True
