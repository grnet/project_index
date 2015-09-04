# Copyright (C) 2014 GRNET S.A.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# enable DEBUG for development
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['127.0.0.1']
ADMINS = (
    ('example', 'foo@example.org'),
)

MANAGERS = ADMINS


# reset the secret key. THIS IS AN EXAMPLE.
SECRET_KEY = 'm4r29he&amp;!kwfj$8v##y=4hz7fl3a03645uu(99g!7*u4v3e&amp;)5'

# db connection info
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',
        'NAME': 'project_index',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

BRANDING = {
    'project_name': 'project_index',
    'name': 'Grnet Noc',
    'logo': 'grnet_logo.png',
    'facebook': 'https://www.facebook.com/noc.grnet.gr',
    'twitter': 'https://twitter.com/grnetnoc',
    'website': 'https://noc.grnet.gr'
}

WIKI = {
    'url': 'http://wiki.noc.grnet.gr',
    'parent_dir': '/Ανάπτυξη/Τεκμηρίωση',
    'databases_dir': '/Βάσεις Δεδομένων/',
    'hosts_dir': '/Hosts/',
    'cronjobs_dir': '/Cronjobs/',
    'projects_dir': '/Projects/',
    'project_category': 'Projects',
    'host_category': 'Hosts',
    'cronjob_category': 'Cronjobs',
    'database_category': 'Βάσεις Δεδομένων'
}

# handle media and static files serving
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
