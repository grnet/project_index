from django.conf.urls import patterns, url
from index.views import instance_views as views

urlpatterns = patterns(
    '',
    url(
        r'^project-state/(?P<instance_id>\w+)/$',
        views.get_project_state, name='project-state'),
)
