from django.conf.urls import patterns, url
from index.views import databases_views

urlpatterns = patterns(
    '',
    url(r'^detail/(?P<id>\d+)/$', databases_views.detail, name='detail'),
    url(r'^$', databases_views.list, name='list'),
)
