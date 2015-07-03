from django.conf.urls import patterns, url
from index.views import projects_views as views
urlpatterns = patterns(
    '',
    url(r'^detail/(?P<project_slug>[\w-]+)/$', views.detail, name='detail'),
    url(r'^$', views.list, name='list'),
)
