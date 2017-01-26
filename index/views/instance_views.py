import datetime
import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from index.models import Project, Instance

from ..utils.reposervice.status import PhabricatorRetriever

def get_project_state(request, instance_id):
    """
    Returns all commits made on branch 'master' that have been
    made after the latest deployment on an instance.

    :param request: The HTTP request object
    :type request: :class: `django.http.HttpRequest`

    :param instance_id: The id of the instance
    :type instance_id: int

    :returns: `django.http.HttpResponse`,
    `django.http.Http404` - depending on whether the request was valid or not
    """

    instance = get_object_or_404(Instance, pk=instance_id)

    project_slug = request.GET.get('project')
    project = get_object_or_404(Project, slug=project_slug)

    repo = project.deployment_repo

    retr = PhabricatorRetriever(repo.url)
    commits = retr.get_recent_commits()

    try:
        instance_hash = instance.deploymentinfo_set.all()[0].commit_hash
    except IndexError:
        commits = dict()

    response = []
    for commit in commits.values():
        if commit['identifier'] == instance_hash:
            break
        response.append({
            'identifier': commit['identifier'],
            'summary': commit['summary'],
            'author': commit['author'],
            'message': commit['message'],
            'date': datetime.datetime.fromtimestamp(
                commit['authorEpoch']).strftime('%c')
        })

    return HttpResponse(json.dumps(response), content_type='application/json')
