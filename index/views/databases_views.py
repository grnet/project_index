from django.shortcuts import render, get_object_or_404
from index.models import Database


def list(request):
    return render(request, 'index/database_list.html', {'databases': Database.objects.all().prefetch_related()})

def detail(request, id):
    return render(request, 'index/database_detail.html', {'database': get_object_or_404(Database, id=id)})