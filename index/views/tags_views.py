from django.shortcuts import render, get_object_or_404
from index.models import Tag


def list(request):
    return render(request, 'index/tag_list.html',
                  {'tags': Tag.objects.all().prefetch_related()})


def detail(request, name):
    return render(request, 'index/tag_detail.html',
                  {'tag': get_object_or_404(Tag, name=name)})
