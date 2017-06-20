"""
Views for instance app
"""
import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from index.models import Project, Instance, DeploymentInfo
from index.utils.reposervice.status import PhabricatorRetriever, RetrieverError
from rest_framework import status as req_status


def get_error_status(message):
    return {
        'error': message
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

    status = req_status.HTTP_200_OK
    response = None
    deployment = None

    try:
        deployment = DeploymentInfo.objects.get(pk=depl_id)
    except DeploymentInfo.DoesNotExist:
        status = req_status.HTTP_404_NOT_FOUND
        response = get_error_status(
            'DeploymentInfo with id "{}" not found'.format(depl_id))

    if deployment:
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
            status = req_status.HTTP_400_BAD_REQUEST
            response = get_error_status('API Error: {}'.format(exc.args[0]))
        else:
            commits = [retr.get_commit_lite_dict(commit)
                       for commit in commits[1:]]
            response = {
                'commits': commits
            }

    return HttpResponse(
        json.dumps(response),
        status=status,
        content_type='application/json')


def get_undeployed_commits(request, instance_id):
    """
    Returns all commits made on branch 'master' that have been
    made after the latest deployment on an instance.

    :param instance_id: The id of the instance
    :type instance_id: int

    :returns: `django.http.HttpResponse`,
    `django.http.Http404` - depending on whether the request was valid or not
    """

    status = req_status.HTTP_200_OK
    response = None
    project = None
    instance = None

    try:
        instance = Instance.objects.get(pk=instance_id)
    except Instance.DoesNotExist:
        status = req_status.HTTP_404_NOT_FOUND
        response = get_error_status(
            'Instance with id "{}" does not exist'.format(instance_id))

    project_slug = request.GET.get('project')
    try:
        project = Project.objects.get(slug=project_slug)
    except Project.DoesNotExist:
        status = req_status.HTTP_404_NOT_FOUND
        response = get_error_status(
            'Project with slug "{}" does not exist'.format(project_slug))

    if project and instance:
        repo = project.deployment_repo
        response = {}
        try:
            retr = PhabricatorRetriever(repo.url)
            commits = retr.get_recent_commits()
            instance_hash = instance.deploymentinfo_set.all()[0].commit_hash
        except AttributeError:
            status = req_status.HTTP_404_NOT_FOUND
            response = get_error_status('No deployable repo(s) found')
        except IndexError:
            status = req_status.HTTP_404_NOT_FOUND
            response = get_error_status('No deployment info found')
        except RetrieverError as exc:
            status = req_status.HTTP_400_BAD_REQUEST
            response = get_error_status('API Error: {}'.format(exc.args[0]))
        except Exception as exc:
            status = req_status.HTTP_500_INTERNAL_SERVER_ERROR
            response = get_error_status(exc.args[0])
        else:
            response['commits'] = []

            for commit in commits:
                if commit['identifier'] == instance_hash:
                    break
                response['commits'] = (
                    response['commits'] + [retr.get_commit_lite_dict(commit)])
    return HttpResponse(
        json.dumps(response),
        status=status,
        content_type='application/json'
    )
