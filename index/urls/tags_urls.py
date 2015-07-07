from django.conf.urls import patterns, url
from index.views import tags_views

urlpatterns = patterns(
    '',
    url(r'^detail/(?P<name>[\w]+)/$', tags_views.detail, name='detail'),
    url(r'^$', tags_views.list, name='list'),
)
