from django.conf.urls import patterns, url
from index.views import wiki_views

urlpatterns = patterns(
    '',
    url(r'^project/detail/(?P<project_slug>[\w-]+)/$', wiki_views.project_detail, name='project_detail'),
    url(r'^cronjob/detail/(?P<cronjob_id>[\w-]+)/$', wiki_views.cronjob_detail, name='cronjob_detail'),
    url(r'^database/detail/(?P<database_id>[\w-]+)/$', wiki_views.database_detail, name='database_detail'),
    url(r'^host/detail/(?P<host_id>[\w-]+)/$', wiki_views.host_detail, name='host_detail'),
    url(r'^wikilogin/(?P<project_slug>[\w-]+)$', wiki_views.wikilogin, name='wikilogin'),
)
