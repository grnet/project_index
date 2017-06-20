from django.conf import settings
from django.core.urlresolvers import reverse
from django.conf import settings


def branding(request):
    return {
        'branding': settings.BRANDING,
    }


def wiki(request):
    return {
        'wiki_urls': settings.WIKI,
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


def sentry(request):
    return settings.SENTRY


def settings_vars(_):
    """
    Context processor.
    Returns variables from `local_settings` in templates
    to enable opt-in features

    :returns: the extra variables from `settings`
    :rtype: dict
    """
    return {
        'DEPLOYMENT_FEATURES_ENABLED': getattr(
            settings, 'DEPLOYMENT_FEATURES_ENABLED', False)
    }
