from django.shortcuts import render, get_object_or_404
from index.models import Project


def detail(request, project_slug):
    return render(request, 'wiki.html', {'project': get_object_or_404(Project, slug=project_slug)})