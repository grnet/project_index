from django.shortcuts import render, get_object_or_404
from index.models import Project


def list(request):
    return render(request, 'index/list.html', {'projects': Project.objects.all().prefetch_related()})


def detail(request, project_slug):
    return render(request, 'index/detail.html', {'project': get_object_or_404(Project, slug=project_slug)})
