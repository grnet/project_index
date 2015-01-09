from django.shortcuts import render, get_object_or_404
from notes.models import Note


def list(request):
    return render(request, 'notes/list.html', {'notes': Note.objects.all()})


def detail(request, id):
    return render(request, 'notes/detail.html', {'note': get_object_or_404(Note, id=id)})
