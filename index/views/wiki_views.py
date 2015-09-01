from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import redirect
from index.models import Project, Cronjob, Database, Host
from index.forms import WikiLoginForm


def project_detail(request, project_slug):
    return render(request, 'project_wiki.html', {'project': get_object_or_404(Project, slug=project_slug)})

def wikilogin(request, project_slug):
    return  redirect('https://wiki.noc.grnet.gr/'+project_slug+'?action=edit')

def cronjob_detail(request, cronjob_id):
    return render(request, 'cronjob_wiki.html', {'cronjob': get_object_or_404(Cronjob, id=cronjob_id)})

def database_detail(request, database_id):
    return render(request, 'database_wiki.html', {'database': get_object_or_404(Database, id=database_id)})

def host_detail(request, host_id):
    return render(request, 'host_wiki.html', {'host': get_object_or_404(Host, id=host_id)})