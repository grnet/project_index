from django.conf.urls import patterns, url
from index.views import databases_views

urlpatterns = patterns(
    '',
    url(r'^$', databases_views.list, name='list'),
)
