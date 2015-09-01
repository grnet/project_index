from django.conf.urls import patterns, url
from index.views import wiki_views

urlpatterns = patterns(
    '',
    url(r'^detail/(?P<project_slug>[\w-]+)/$', wiki_views.detail, name='detail'),
    url(r'^wikilogin/(?P<project_slug>[\w-]+)$', wiki_views.wikilogin, name='wikilogin'),
)
