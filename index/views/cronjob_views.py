from django.shortcuts import render, get_object_or_404
from index.models import Cronjob


def list(request):
    return render(request, 'index/cronjob_list.html',
                  {'cronjobs': Cronjob.objects.all().prefetch_related()})


def detail(request, id):
    return render(request, 'index/cronjob_detail.html',
                  {'cronjob': get_object_or_404(Cronjob, id=id)})
