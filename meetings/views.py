from django.shortcuts import render, get_object_or_404
from meetings.models import Meeting


def list(request):
    return render(request, 'meetings/list.html', {'meetings': Meeting.objects.all()})


def detail(request, id):
    print 'asd'
    return render(request, 'meetings/detail.html', {'meeting': get_object_or_404(Meeting, id=id)})
