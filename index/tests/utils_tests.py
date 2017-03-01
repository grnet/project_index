"""
Tests for `index.utils.reposervice.status` module
"""
# pylint: disable=C0111,C0103,W0621,R0201

import json
import os
import urllib2
import re
import sys
from collections import OrderedDict
from functools import partial
from urllib import unquote

import random
import pytest
import string
from mock import Mock


from index.utils.reposervice.status import (
    ProjectStatusRetriever, PhabricatorRetriever, RetrieverError)

thismodule = sys.modules[__name__]

DATA_PATH = os.path.join(os.path.dirname(thismodule.__file__), 'data')

REPO_NAMES = [
    'repoone',
]

# A NOTE ABOUT DATA FILES
# Every repository defined below contains data that derive from an actual
# request made in the phabricator repo. This is so that we are mocking
# as accurately as possible.
REPOS = [
    {
        'name': repo_name.upper(),
        'url': 'https://phab.noc.grnet.gr/diffusion/{}/repoone.git'.format(
            repo_name.upper()),
        'recentcommits': os.path.join(
            DATA_PATH, '{}_recentcommits.json'.format(repo_name.lower())),
    } for repo_name in REPO_NAMES
]


def commit_phid(commit_name):
    """
    Accepts a commit name and returns a (deterministic) phid.

    Convention:
    phid = 'PHID-CMIT-<commitName>'
    """

    return 'PHID-CMIT-{}'.format(commit_name)


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


@pytest.fixture(params=REPOS)
def data(request):

    recentcommits = OrderedDict()
    with open(request.param.get('recentcommits'), 'r') as inp:
        commits = json.load(inp)
        recentcommits = OrderedDict(
            sorted(commits.items(), key=lambda t: int(t[0])))

    return {
        'name': request.param.get('name'),
        'url': request.param.get('url'),
        'recentcommits': recentcommits,
    }


@pytest.fixture
def phid_lookup(data, request):

    def is_repo(name):
        return len(name.split(data.get('name'))[1]) == 0

    def get_repo(url, name):
        return {
            'phid': 'PHID-REPO-{}-r4nd0mstr1ng'.format(name.lower()),
            'uri': '{}/diffusion/{}'.format(url, name.replace('r', '')),
            'typeName': 'Repository',
            'name': name,
            'fullname': '{} something'.format(name),
            'status': 'open'
        }

    def get_commit(url, name):
        return {
            'phid': commit_phid(name),
            'uri': '{}/diffusion/{}'.format(url, name.replace('r', '')),
            'typeName': 'Diffusion Commit',
            'name': name,
            'fullname': '{}: A commit message'.format(name),
            'status': 'open'
        }

    names = [
        name for name in re.split(
            r'names\[[0-9]+\]=(\w+)&*', unquote(request.get_data()))
        if name and 'token' not in name]

    return json.dumps({
        'result': {
            name:
                get_repo(request.get_host(), name) if is_repo(name) else
                get_commit(request.get_host(), name) for name in names
            }
    })


@pytest.fixture
def diffusion_getrecentcommitsbypath(data, request):

    match = re.search(r'limit=([0-9]+)', request.get_data())
    limit = match.groups(0)[0]

    commits = list()

    max_commits = len(data.get('recentcommits').keys())
    limit = int(limit) if int(limit) < max_commits else max_commits

    for i in range(int(limit)):
        commits.append(data.get('recentcommits').get(str(i)))
    return json.dumps({'result': commits})


@pytest.fixture
def diffusion_querycommits(data, request):

    def get_commit_full(name):
        # useless fields are ommited
        return {
            commit_phid(name): {
                "id": int(''.join(
                    random.choice(string.digits) for _ in range(5))),
                "identifier": re.sub('r[A-Z]+', '', name),
                "summary": "Some interesting summary",
                "author": "Mighty Programmer <mighty@programmer.com>",
                "phid": commit_phid(name),
            }
        }

    id_map = dict()
    ret_data = dict()
    names = [
        name for name in re.findall(
            r'names\[[0-9]+\]=(r\w+)&*', unquote(request.get_data()))
        if name and 'token' not in name]

    # phabricator returns the commits in an order defined by it's
    # internal mapping. To emulate this, shuffle the commits.
    random.shuffle(names)
    for name in names:
        name = name.split('&')[0]
        id_map.update({name: commit_phid(name)})
        ret_data.update(get_commit_full(name))

    return json.dumps({
        'result': {
            'data': ret_data,
            'identifierMap': id_map
        }})


class TestPhabricatorRetriever(object):

    @staticmethod
    def monkeypatch_urllib_urlopen(monkeypatch, data):

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
            urlopen.read = partial(endpoint_func, data, req_obj)
            return urlopen

        monkeypatch.setattr(
            'index.utils.reposervice.status.urlopen', mock_urlopen)

    def test_init(self, data, monkeypatch):
        self.monkeypatch_urllib_urlopen(monkeypatch, data)

        PhabricatorRetriever(data.get('url'))

    def test_failed_init(self, data, monkeypatch):
        self.monkeypatch_urllib_urlopen(monkeypatch, data)

        with pytest.raises(RetrieverError):
            PhabricatorRetriever('aaa')

    def test_get_recent_commits(self, data, monkeypatch):
        self.monkeypatch_urllib_urlopen(monkeypatch, data)

        retriever = PhabricatorRetriever(data.get('url'))

        # try to retrieve 20 most recent commits
        commits = retriever.get_recent_commits()
        assert len(commits) == 20
        for index in range(20):
            assert (
                data.get('recentcommits').values()[index][1:] ==
                commits[index].get('phid').split('-')[-1])

    def test_get_commits_between_refs(self, monkeypatch, data):

        def hash_from_name(value):
            return value.split(data.get('name'))[1]

        self.monkeypatch_urllib_urlopen(monkeypatch, data)

        retriever = PhabricatorRetriever(data.get('url'))

        recentcommits = data.get('recentcommits')

        existing_refs = [
            hash_from_name(recentcommits.values()[8][1:]),
            hash_from_name(recentcommits.values()[4][1:])
        ]

        commits = retriever.get_commits_between_refs(
            existing_refs[0], existing_refs[1])
        assert len(commits) == 5
        for index in range(5):
            assert(
                hash_from_name([
                    comm for comm in reversed(recentcommits.values()[4:9])
                ][index]) == commits[index].get('identifier'))

        with pytest.raises(RetrieverError):
            commits = retriever.get_commits_between_refs(
                'invalid_ref1', 'invalid_ref2')

        with pytest.raises(RetrieverError):
            commits = retriever.get_commits_between_refs(
                existing_refs[0], 'invalid_ref2')

        commits = retriever.get_commits_between_refs(
            existing_refs[1], existing_refs[0])
        assert commits == []
