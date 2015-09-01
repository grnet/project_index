from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import redirect
from index.models import Project
from index.forms import WikiLoginForm


def detail(request, project_slug):
    form = WikiLoginForm()
    return render(request, 'wiki.html', {'project': get_object_or_404(Project, slug=project_slug), 'form': form})

def wikilogin(request, project_slug):
    return  redirect('https://wiki.noc.grnet.gr/'+project_slug+'?action=edit')