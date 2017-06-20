"""
Urls for `instance`s
"""
from django.conf.urls import url
from django.conf import settings
from index.views import instance_views as views

urlpatterns = [
]

if getattr(settings, 'DEPLOYMENT_FEATURES_ENABLED', None):
    urlpatterns += [
        url(
            r'^undeployed-commits/(?P<instance_id>\w+)/$',
            views.get_undeployed_commits, name='undeployed-commits'),
        url(
            r'deployment-details/(?P<depl_id>\w+)/$',
            views.get_deployment_details, name='deployment-details'),
    ]
