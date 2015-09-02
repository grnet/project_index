# Copyright (C) 2010-2014 GRNET S.A.
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

from django.conf.urls import patterns, include, url
from django.contrib import admin

from index.urls import project_urls as index_urls
from index.urls import tags_urls
from index.urls import hosts_urls
from index.urls import cronjob_urls
from index.urls import wiki_urls
from index.urls import database_urls

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(index_urls)),
    url(r'^tags/', include(tags_urls, namespace='tags')),
    url(r'^hosts/', include(hosts_urls, namespace='hosts')),
    url(r'^cronjobs/', include(cronjob_urls, namespace='cronjobs')),
    url(r'^wiki/', include(wiki_urls, namespace='wiki')),
    url(r'^databases/', include(database_urls, namespace='databases')),
)
