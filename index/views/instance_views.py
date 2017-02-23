import datetime
import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from index.models import Project, Instance

from ..utils.reposervice.status import PhabricatorRetriever, RetrieverError

def get_deployment_details(request, depl_id):
    """
    Returns the details for a specific deployment.


    :param depl_id: the `DeploymentInfo` object id
    :type depl_id: int

    :returns: `django.http.HttpResponse`
    """


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

    def get_error_status(message):
        """
        Returns an error description dictionary

        :returns: dict - the dictionary describing the error
        """
        return {
            'type': 'error',
            'message': message
        }

    response = dict()
    commits = dict()
    instance = get_object_or_404(Instance, pk=instance_id)

    project_slug = request.GET.get('project')
    project = get_object_or_404(Project, slug=project_slug)

    repo = project.deployment_repo

    try:
        retr = PhabricatorRetriever(repo.url)
        commits = retr.get_recent_commits()
        instance_hash = instance.deploymentinfo_set.all()[0].commit_hash
    except AttributeError:
        response['status'] = get_error_status('No deployable repo(s) found')
    except IndexError:
        response['status'] = get_error_status('No deployment info found')
    except RetrieverError as e:
        response['status'] = get_error_status('API Error: {}'.format(e.args[0]))
    except Exception as e:
        response['status'] = get_error_status(e.args[0])
    else:
        response['status'] = {
            'type': 'success',
            'message': 'Data retrieved successfully',
        }
        response['data'] = []

        for commit in commits.values():
            if commit['identifier'] == instance_hash:
                break
            response['data'] = response['data'] + [{
                'identifier': commit['identifier'],
                'summary': commit['summary'],
                'author': commit['author'],
                'message': commit['message'],
                'date': datetime.datetime.fromtimestamp(
                    commit['authorEpoch']).strftime('%c')
            }]

    return HttpResponse(json.dumps(response), content_type='application/json')
