from django.conf.urls import patterns, url
from index.views import cronjob_views

urlpatterns = patterns(
    '',
    url(r'^detail/(?P<id>\d+)/$', cronjob_views.detail, name='detail'),
    url(r'^$', cronjob_views.list, name='list'),
)
