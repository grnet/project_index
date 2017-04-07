"""
Urls for `instance`s
"""
from django.conf.urls import patterns, url
from index.views import instance_views as views

urlpatterns = patterns(
    '',
    url(
        r'^undepl-commits/(?P<instance_id>\w+)/$',
        views.get_undeployed_commits, name='undepl-commits'),
)
