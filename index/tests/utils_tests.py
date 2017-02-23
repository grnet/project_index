"""
Tests for `index.utils.reposervice.status` module
"""
# pylint: disable=C0111,W0621,R0201

import json
import urllib2
import re
import sys
from functools import partial
from urllib import unquote

import pytest
from mock import Mock

from index.utils.reposervice.status import (
    ProjectStatusRetriever, PhabricatorRetriever, RetrieverError)

thismodule = sys.modules[__name__]

REPO_URLS_FOR_NAMES = [
    {
        'url': 'https://phab.noc.grnet.gr/diffusion/GMGR/ganetimgr.git',
        'name': 'rGMGR',
        'api_url': 'https://phab.noc.grnet.gr/api',
    },
    {
        'url': 'https://phab.noc.grnet.gr/diffusion/GMGR/ganetimgr.git',
        'name': 'rGMGR',
        'api_url': 'https://phab.noc.grnet.gr/api',
    }
]


def test_projectstatusretriever():

    class SomeRetriever(ProjectStatusRetriever):

        def authorize_request(self, **kwargs):
            headers = kwargs.get('headers')
            headers.update({'Token': self.api_auth})
            return (kwargs.get('data'), headers)

    auth_token = '$0M34uTHT0K3N'
    retriever = SomeRetriever(
        'https://example.com', auth_token)

    data = {
        'some_key': 'some_value',
        'some_key2': [
            'some_value1',
            'some_value2'
        ]
    }
    headers = {'Content_type': 'application/json'}
    endpoint = 'api'

    req = retriever.build_request(
        endpoint=endpoint, data=data, headers=headers)

    assert isinstance(req, urllib2.Request)
    assert req.data == (
        'some_key=some_value&some_key2=some_value1&some_key2=some_value2')
    assert req.get_full_url() == 'https://example.com/api'
    assert req.headers == headers


def phid_lookup(data):

    def get_repo(url, name):
        return {
            'phid': 'PHID-REPO-{}-r4nd0mstr1ng'.format(name.lower()),
            'uri': '{}/diffusion/{}'.format(url, name.replace('r', '')),
            'typeName': 'Repository',
            'name': name,
            'fullname': '{} something'.format(name),
            'status': 'open'
        }

    names = [
        name for name in re.split(
            r'names\[[0-9]+\]=(\w+)&*', unquote(data.get_data()))
        if name and 'token' not in name]

    return json.dumps({
        'result': {
            name: get_repo(data.get_host(), name) for name in names
        }
    })


@pytest.fixture(params=REPO_URLS_FOR_NAMES)
def data(request):
    return request.param


@pytest.fixture(autouse=True)
def monkeypatch_urllib_urlopen(monkeypatch):

    def mock_urlopen(*args):

        req_obj = args[0]
        endpoint = req_obj.get_full_url().split(
            req_obj.get_host())[1].replace('/api/', '')

        try:
            endpoint_func = getattr(thismodule, endpoint.replace('.', '_'))
        except:
            raise RuntimeError(
                'Endpoint {} has not been tested yet'.format(endpoint))
        urlopen = Mock()
        urlopen.read = partial(endpoint_func, req_obj)
        return urlopen

    monkeypatch.setattr(
        'index.utils.reposervice.status.urlopen', mock_urlopen)


class TestPhabricatorRetriever(object):

    #  def test_get_repo_name(self, data):
    #      if not ('http' in data.get('url') or 'https' in data.get('url')):
    #          with pytest.raises(RetrieverError):
    #              PhabricatorRetriever.get_repo_name(data.get('url'))
    #      else:
    #          name = PhabricatorRetriever.get_repo_name(data.get('url'))
    #          assert name == data.get('name')
    #
    #  def test_get_api_url(self, data):
    #      assert PhabricatorRetriever.get_api_url(
    #          data.get('url')) == data.get('api_url')
    #
    #  def test_get_commit_name(self, data)

    def test_init(self, data):

        PhabricatorRetriever(data.get('url'))
