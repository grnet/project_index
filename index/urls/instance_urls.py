"""
Urls for `instance`s
"""
from django.conf.urls import patterns, url
from index.views import instance_views as views

urlpatterns = patterns(
    '',
    url(
        r'^undeployed-commits/(?P<instance_id>\w+)/$',
        views.get_undeployed_commits, name='undeployed-commits'),
    url(
        r'deployment-details/(?P<depl_id>\w+)/$',
        views.get_deployment_details, name='deployment-details'),
)
