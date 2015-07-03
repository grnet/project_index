from django.conf.urls import patterns, url
from index.views import hosts_views

urlpatterns = patterns(
    '',
    url(r'^detail/(?P<id>\d+)/$', hosts_views.detail, name='detail'),
    url(r'^$', hosts_views.list, name='list'),
)
