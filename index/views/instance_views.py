import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from index.models import Project, Instance, DeploymentInfo

from index.utils.reposervice.status import PhabricatorRetriever, RetrieverError


def get_error_status(message):
    """
    Returns an error description dictionary

    :returns: the dictionary describing the error
    :rtype: dict
    """
    return {
        'type': 'error',
        'message': message
    }


def get_deployment_details(request, depl_id):
    """
    Returns the commits for a specific deployment.

    This is done by finding which commits are between two different
    deployments & fetching all these commits (including the deployed
    commit).

    :param depl_id: the `DeploymentInfo` object id
    :type depl_id: int

    :returns: `django.http.HttpResponse`
    """

    response = dict()
    deployment = get_object_or_404(DeploymentInfo, pk=depl_id)
    deployments = list(
        deployment.instance.deploymentinfo_set.all().order_by('date'))
    previous_depl = deployments[
        deployments.index(deployment) - 1] if (
            deployments.index(deployment) - 1 >= 0) else None

    try:
        hashes = (
            getattr(previous_depl, 'commit_hash', None),
            deployment.commit_hash)
        repo_url = deployment.instance.project.deployment_repo.url
        retr = PhabricatorRetriever(repo_url)
        commits = retr.get_commits_between_refs(*hashes)
    except RetrieverError as exc:
        response['status'] = get_error_status(
            'API Error: {}'.format(exc.args[0]))
    else:
        response['status'] = {
            'type': 'success',
            'message': 'Data retrieved successfully',
        }
        response['data'] = [retr.get_commit_lite_dict(commit)
                            for commit in commits[1:]]
    return HttpResponse(json.dumps(response), content_type='application/json')


def get_undeployed_commits(request, instance_id):
    """
    Returns all commits made on branch 'master' that have been
    made after the latest deployment on an instance.

    :param instance_id: The id of the instance
    :type instance_id: int

    :returns: `django.http.HttpResponse`,
    `django.http.Http404` - depending on whether the request was valid or not
    """

    response = dict()
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
    except RetrieverError as exc:
        response['status'] = get_error_status(
            'API Error: {}'.format(exc.args[0]))
    except Exception as exc:
        response['status'] = get_error_status(exc.args[0])
    else:
        response['status'] = {
            'type': 'success',
            'message': 'Data retrieved successfully',
        }
        response['data'] = []

        for commit in commits:
            if commit['identifier'] == instance_hash:
                break
            response['data'] = (
                response['data'] + [retr.get_commit_lite_dict(commit)])
    return HttpResponse(json.dumps(response), content_type='application/json')
