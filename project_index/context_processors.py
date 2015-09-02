from django.conf import settings
from django.core.urlresolvers import reverse


def branding(request):
    return {
        'branding': settings.BRANDING,
    }


def menu(request):
    path = request.path
    menu = [
        {'url': reverse('list'), 'name': 'Projects'},
        {'url': reverse('tags:list'), 'name': 'Tags'},
        {'url': reverse('hosts:list'), 'name': 'Hosts'},
        {'url': reverse('cronjobs:list'), 'name': 'Cronjobs'},
        {'url': reverse('databases:list'), 'name': 'Databases'},
    ]
    for m in menu:
        if m.get('url') == path:
            m.update({'active': 'active'})
    return {'menu': menu}
