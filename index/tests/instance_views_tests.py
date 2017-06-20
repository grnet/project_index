"""
Tests for `index.utils.reposervice.status` module
"""
# pylint: disable=C0111,C0103,W0621,R0201

from collections import OrderedDict

import datetime
import json
import pytest

from index.models import (
    Project, Host, Instance, DeploymentInfo, Repository)
from index.utils.reposervice.status import RetrieverError
from django.core.urlresolvers import reverse


class TestInstanceUrls(object):

    @staticmethod
    def monkeypatch_PhabricatorRetriever(monkeypatch):

        class MockPHRetriever(object):

            @staticmethod
            def produce_commit(commit_hash):

                return OrderedDict([
                    ('identifier', commit_hash), ('summary', 'Some summary'),
                    ('author', 'Some author'), ('message', 'Some message'),
                    ('authorEpoch', '1491919872')])

            def __init__(self, url):
                # When the URL has the word `error` in it,
                # raise a `RetrieverError` on purpose
                # to test other cases
                self.commit_data = [
                    self.produce_commit(h_val) for h_val in [
                        'commit_hash_{}'.format(str(ind)) for ind in range(70)]
                ]

                if 'error' in url:
                    raise RetrieverError('Fixed url for error')
                self.url = url
                super(MockPHRetriever, self).__init__()

            def get_recent_commits(self, number=20):
                # When the URL has the word `otherexc` in it,
                # raise a `ValueError` on purpose
                # to test other cases
                if 'otherexc' in self.url:
                    raise ValueError('Fixed url for error')

                return self.commit_data[:number]

            def get_commits_between_refs(self, _, __, max_refs=50):
                return self.commit_data[:max_refs]

            def get_commit_lite_dict(self, commit):
                return commit

        monkeypatch.setattr(
            'index.views.instance_views.PhabricatorRetriever', MockPHRetriever)

    @pytest.fixture
    @pytest.mark.django_db
    def dummy_project(self):
        project = Project.objects.create(
            name='Dummy Project', slug='dummy-project')
        Repository.objects.create(
            name='Dummy Repo', url='https://example.com/repo/dummy.git',
            project=project, public=True, deployable=True)
        return project

    @pytest.fixture
    @pytest.mark.django_db
    def dummy_error_project(self):
        project = Project.objects.create(
            name='Dummy Error Project', slug='dummy-error')
        Repository.objects.create(
            name='Dummy Repo', url='https://example.com/repo/error.git',
            project=project, public=True, deployable=True)
        return project

    @pytest.fixture
    @pytest.mark.django_db
    def dummy_host(self):
        host = Host.objects.create(
            name='Dummy Host')
        return host

    @pytest.fixture
    @pytest.mark.django_db
    def dummy_instance(self, dummy_project, dummy_host):
        return Instance.objects.create(
            project=dummy_project, host=dummy_host)

    @pytest.mark.django_db
    def test_get_deployment_details_wrong_depl(self, client):
        assert client.get(
            reverse('instances:deployment-details', kwargs={'depl_id': 4})
        ).status_code == 404

    @pytest.mark.django_db
    def test_get_deployment_details_fixed_error(
            self, client, monkeypatch, dummy_host, dummy_error_project):

        self.monkeypatch_PhabricatorRetriever(monkeypatch)

        instance = Instance.objects.create(
            project=dummy_error_project, host=dummy_host)
        depl_info = DeploymentInfo.objects.create(
            instance=instance, date=datetime.datetime.today(),
            commit_hash="commit_hash_1", user='god')
        resp = client.get(
            reverse(
                'instances:deployment-details',
                kwargs={'depl_id': depl_info.pk}))
        assert resp.status_code == 400

    @pytest.mark.django_db
    def test_get_deployment_details_only_one_depl(
            self, client, monkeypatch, dummy_instance):

        self.monkeypatch_PhabricatorRetriever(monkeypatch)

        depl_info = DeploymentInfo.objects.create(
            instance=dummy_instance, date=datetime.datetime.today(),
            commit_hash="commit_hash_1", user='god')
        resp = client.get(
            reverse(
                'instances:deployment-details',
                kwargs={'depl_id': depl_info.pk}))
        assert resp.status_code == 200

    @pytest.mark.django_db
    def test_get_deployment_details_only_many_depls(
            self, client, monkeypatch, dummy_instance):

        self.monkeypatch_PhabricatorRetriever(monkeypatch)

        depl_info = DeploymentInfo.objects.create(
            instance=dummy_instance, date=datetime.datetime.today(),
            commit_hash="commit_hash_2", user='god')
        depl_info = DeploymentInfo.objects.create(
            instance=dummy_instance, date=(
                datetime.datetime.today() - datetime.timedelta(days=1)),
            commit_hash="commit_hash_1", user='god')
        resp = client.get(
            reverse(
                'instances:deployment-details',
                kwargs={'depl_id': depl_info.pk}))
        assert resp.status_code == 200

    @pytest.mark.django_db
    def test_get_undeployed_commits_wrong_instance(self, client, monkeypatch):

        self.monkeypatch_PhabricatorRetriever(monkeypatch)

        assert client.get(
            reverse('instances:undeployed-commits', kwargs={'instance_id': 4})
        ).status_code == 404

    @pytest.mark.django_db
    def test_get_undeployed_commits_wrong_project(
            self, client, monkeypatch, dummy_instance):

        self.monkeypatch_PhabricatorRetriever(monkeypatch)

        assert client.get('{}?project="wrong-slug"'.format(
            reverse(
                'instances:undeployed-commits',
                kwargs={'instance_id': dummy_instance.pk}
            ))).status_code == 404

    @pytest.mark.django_db
    def test_get_undeployed_commits_no_depl_repo(
            self, client, monkeypatch, dummy_instance):

        self.monkeypatch_PhabricatorRetriever(monkeypatch)

        repo = dummy_instance.project.deployment_repo
        repo.deployable = False
        repo.save()

        resp = client.get('{}?project=dummy-project'.format(
            reverse(
                'instances:undeployed-commits',
                kwargs={'instance_id': dummy_instance.pk}
            )))
        content = json.loads(resp.content)
        assert resp.status_code == 404
        assert content['error'] == 'No deployable repo(s) found'

    @pytest.mark.django_db
    def test_get_undeployed_commits_index_error(
            self, client, monkeypatch, dummy_instance):

        # You don't create a `DeploymentInfo` so code getting
        # the 'instance_hash' will crash
        self.monkeypatch_PhabricatorRetriever(monkeypatch)

        resp = client.get('{}?project=dummy-project'.format(
            reverse(
                'instances:undeployed-commits',
                kwargs={'instance_id': dummy_instance.pk}
            )))
        content = json.loads(resp.content)
        assert resp.status_code == 404
        assert content['error'] == 'No deployment info found'

    @pytest.mark.django_db
    def test_get_undeployed_commits_retr_error(
            self, client, monkeypatch, dummy_host, dummy_error_project):

        self.monkeypatch_PhabricatorRetriever(monkeypatch)
        instance = Instance.objects.create(
            project=dummy_error_project, host=dummy_host)
        DeploymentInfo.objects.create(
            instance=instance, date=datetime.datetime.today(),
            commit_hash="commit_hash_1", user='god')
        resp = client.get('{}?project=dummy-error'.format(
            reverse(
                'instances:undeployed-commits',
                kwargs={'instance_id': instance.pk}
            )))
        content = json.loads(resp.content)
        assert resp.status_code == 400
        assert content['error'] == (
            'API Error: Fixed url for error')

    @pytest.mark.django_db
    def test_get_undeployed_commits_other_error(
            self, client, monkeypatch, dummy_project, dummy_host):

        self.monkeypatch_PhabricatorRetriever(monkeypatch)
        repo = dummy_project.repository_set.all()[0]
        repo.url += 'otherexc'
        repo.save()
        instance = Instance.objects.create(
            project=dummy_project, host=dummy_host)
        DeploymentInfo.objects.create(
            instance=instance, date=datetime.datetime.today(),
            commit_hash="commit_hash_1", user='god')
        resp = client.get('{}?project=dummy-project'.format(
            reverse(
                'instances:undeployed-commits',
                kwargs={'instance_id': instance.pk}
            )))
        content = json.loads(resp.content)
        assert resp.status_code == 500
        assert content['error'] == 'Fixed url for error'

    @pytest.mark.django_db
    def test_get_undeployed_commits_no_error(
            self, client, monkeypatch, dummy_instance):

        self.monkeypatch_PhabricatorRetriever(monkeypatch)

        DeploymentInfo.objects.create(
            instance=dummy_instance, date=datetime.datetime.today(),
            commit_hash="commit_hash_10", user='god')
        resp = client.get('{}?project=dummy-project'.format(
            reverse(
                'instances:undeployed-commits',
                kwargs={'instance_id': dummy_instance.pk}
            )))
        content = json.loads(resp.content)
        assert resp.status_code == 200
        commits = content['commits']
        assert len(commits) == 10
        for comm, ind in zip(commits, range(0, 9)):
            assert comm['identifier'] == 'commit_hash_{}'.format(str(ind))
