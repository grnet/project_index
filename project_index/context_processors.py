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
from django.conf import settings
from django.core.urlresolvers import reverse


def branding(request):
        return {
            'branding': settings.BRANDING,
        }


def menu(request):
    path = request.path
    menu = [
        {'url': reverse('notes:list'), 'name': 'Notes'},
        {'url': reverse('list'), 'name': 'Projects'},
        {'url': reverse('tags:list'), 'name': 'Tags'},
    ]
    for m in menu:
        if m.get('url') == path:
            m.update({'active': 'active'})
    return {'menu': menu}
