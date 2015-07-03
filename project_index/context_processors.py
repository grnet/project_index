from django.conf import settings
from django.core.urlresolvers import reverse


def branding(request):
    return {
        'branding': settings.BRANDING,
    }


def menu(request):
    path = request.path
    menu = [
        {'url': reverse('notes:list'), 'name': 'Notes'},
        {'url': reverse('list'), 'name': 'Projects'},
        {'url': reverse('tags:list'), 'name': 'Tags'},
        {'url': reverse('hosts:list'), 'name': 'Hosts'},
    ]
    for m in menu:
        if m.get('url') == path:
            m.update({'active': 'active'})
    return {'menu': menu}
