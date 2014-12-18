from django.shortcuts import render
from notes.models import Note


def list(request):
    return render(request, 'notes/list.html', {'notes': Note.objects.all()})
