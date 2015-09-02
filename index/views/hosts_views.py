from django.shortcuts import render, get_object_or_404
from index.models import Host


def list(request):
    return render(request, 'index/host_list.html',
                  {'hosts': Host.objects.all().prefetch_related()})


def detail(request, id):
    return render(request, 'index/host_detail.html',
                  {'host': get_object_or_404(Host, id=id)})
