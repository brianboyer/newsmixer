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

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/public/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

# Some crazy Django shite
# http://docs.djangoproject.com/en/dev/ref/templates/api/?from=olddocs
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "pie.authentication.context_processors.facebook",
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'facebook.djangofb.FacebookMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'pie.authentication.middleware.FacebookConnectMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'djangodblog.middleware.DBLogMiddleware',
)

ROOT_URLCONF = 'pie.urls'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.flatpages',
    
    'pie.articles',
    'pie.authentication',
    'pie.bumbles',
    'pie.profiles',
    'pie.questions',
    'pie.letters',
    
    'contact_form',#install django-contact-form to your python path, needs python akismet
    'search',      #install django-search to your python path
    'photologue',  #install django-photologue to your python path
    'pressroom',   #install django-pressroom to your python path
    'djangodblog', #install django-db-log to your python path
)

# authentication
AUTH_PROFILE_MODULE = "profiles.UserProfile"
AUTHENTICATION_BACKENDS = (
    'pie.authentication.models.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend', #for auth unit tests
)

#django-search
SEARCH_CRAWLERS = (
    "search.crawlers.models.ModelCrawler",
)
SEARCH_BACKEND = "search.backends.simple"

#django-contact-form
AKISMET_API_KEY = ""

#Cache facebook info for x seconds
FACEBOOK_CACHE_TIMEOUT = 1800

#setting this to true will cause facebook to fail randomly
#only for the masochistic
RANDOM_FACEBOOK_FAIL = False