import abc
import json

from collections import OrderedDict
from urllib import urlencode
from urllib2 import Request, urlopen
from itertools import islice

from django.conf import settings


class RetrieverError(RuntimeError):
    """
    Raised when retriever cannot communicate with the API
    """
    pass


class ProjectStatusRetriever(object):
    """
    Implements an interface which is used to connect with a repository
    management service's (e.g. Phabricator) API and fetch useful information
    about projects hosted there.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, api_url, api_auth):
        """
        Initialize basic required parameters.

        :param api_url: The url of the API endpoint
        :type api_url: str

        :param api_auth: The parameters required for authentication
        :type api_auth: dict()

        :returns: None
        """
        self.api_url = api_url
        self.api_auth = api_auth

    @abc.abstractmethod
    def authorize_request(self, **kwargs):
        """
        Manipulate `data`, `headers` to add whatever is necessary
        to make the request properly authorized

        Override & implement as required.

        Must return a tuple, (data, headers) with the required data

        :returns: tuple
        """
        pass

    def build_request(self, endpoint='', **kwargs):
        """
        Returns a `urllib2.Request` item which is later used to query
        the API. Passes `kwargs['headers']` as request headers and
        `kwargs['data']` into the request headers & data resp.

        :param endpoint: The endpoint path to append to the API
        :type endpoint: str

        :param kwargs: the data used to build the request

        :returns: the request item
        :rtype: :class:`urllib2.Request`
        """

        data = kwargs.get('data') or dict()
        headers = kwargs.get('headers') or dict()

        (data, headers) = self.authorize_request(data=data, headers=headers)
        url = self.api_url.strip('/') + '/' + endpoint

        return Request(url, urlencode(data, doseq=True), headers)


class PhabricatorRetriever(ProjectStatusRetriever):
    """
    Implements a `ProjectStatusRetriever` for the Phabricator
    repository service.

        """

    def __init__(
            self, url, api_token=getattr(settings, 'PHABRICATOR_API_TOKEN')):
        """
        Initializes a `PhabricatorRetriever` by connecting to the remote
        API  and retrieving the repo's name, phid.

        :param url: a phabricator repository url (https only)
        :type url: str

        :param api_token: the phabricator API (Conduit) token
        :type api_token: str

        :raises RetrieverError: when the remote API cannot be reached
        """
        self.repo_phid = ''
        self.repo_name = ''
        super(PhabricatorRetriever, self).__init__(
            self.get_api_url(url), {'api.token': api_token})
        try:
            self.set_repo(url)
        except:
            raise RetrieverError(
                'Cannot initiate PhabricatorRetriever. Did you provide '
                'a valid Phabricator URL? ("{}")'.format(url))

    @staticmethod
    def get_api_url(url):
        """
        Parses a phabricator repository URL (https) and returns the
        api url

        :param url: The phabricator repository url
        :type url: str

        :returns: the phabricator api url
        :rtype: str
        """
        # remove 'https://', split on ('/'), keep the first part (the host),
        # add 'https://' again
        return 'https://' + url.replace('https://', '').split('/')[0] + '/api'

    @staticmethod
    def get_repo_name(url):
        """
        Parses a phabricator repository URL (https, http) and returns the
        repository name

        :param url: The phabricator repository url
        :type url: str

        :returns: The phabricator repository name
        :rtype: str

        :raises RetrieverError: when the repo url is not https / http
        """

        repo_protocol = None
        accepted_protocols = ['https', 'http']
        for protocol in accepted_protocols:
            repo_protocol = protocol if protocol in url else None

        if not repo_protocol:
            raise RetrieverError(
                'Malformed repo url: Only `http`, `https` protocols allowed')

        # remove 'https://', split on ('/'), keep the semi-final part
        return 'r' + url.replace(repo_protocol + '://', '').split('/')[-2]

    @staticmethod
    def get_commit_name(repo_callsign, commit):
        """
        Returns the phabricator "name" for a commit object.

        The name is formed as callsign + commit hash

        :param repo_callsign: the repository phabricator callsign
        :type repo_callsign: str

        :param commit: the commit hash
        :type commit: str

        :returns: the phabricator commit name
        :rtype: str
        """
        return repo_callsign + commit

    def set_repo(self, url):
        """
        Initializes an instance to work on a specific repo.

        :param url: A phabricator repository url
        :type url: str

        """
        self.repo_name = self.get_repo_name(url)
        self.repo_phid = self.get_phids_for_objects(
            [self.repo_name])['result'][self.repo_name]['phid']

    def authorize_request(self, **kwargs):
        """
        Add `self.api_auth` string to request data to authorize it

        :returns: a tuple containing the data and the
        authorized request
        :rtype: tuple
        """
        data = dict(kwargs['data'])
        data.update(self.api_auth)
        return (data, kwargs['headers'])

    def get_phids_for_objects(self, names):
        """
        Returns `phid`s of the given "name"s

        :param names: The "name"s of the objects for which a `phid` should
        be retrieved
        :type names: list

        :returns: the objects' `phid`s
        :rtype: list
        """

        data = {}
        for idx, name in enumerate(names):
            data.update({'names[' + str(idx) + ']': name})

        request = self.build_request('phid.lookup', data=data)
        response = urlopen(request)
        data = json.loads(response.read())
        return data

    def get_recent_commits(self, number=20):
        """
        Makes a request in phabricator "Conduit" API and retrieves the
        latest commits for the repository it is initialized.

        :param number: The number of commits to retrieve
        :type number: int

        :returns: a list with the commits details
        :rtype: list
        """
        r1_data = {
            'callsign': self.repo_name,
            'branch': 'master',
            'limit': number
        }

        r1_request = self.build_request(
            'diffusion.getrecentcommitsbypath', data=r1_data)
        r1_response = urlopen(r1_request)
        r1_data = json.loads(r1_response.read(), object_pairs_hook=OrderedDict)

        data = {}

        for idx, value in enumerate(r1_data['result']):
            data.update({'names[' + str(idx) + ']': value})

        data = {
            'repositoryPHID': self.repo_phid,
            'limit': number,
            'needMessages': True
        }

        request = self.build_request('diffusion.querycommits', data=data)

        response = urlopen(request)

        # use `OrderedDict` to maintain order of commits
        data = json.loads(response.read(), object_pairs_hook=OrderedDict)
        return data['result']['data']

    def get_commits_between_refs(self, ref_start, ref_end, max_refs=50):
        """
        Returns details for the commits between `ref_start`, `ref_end`
        (including those).

        Repeatedly queries the phabricator API to retrieve

        :param ref_start: the commit hash to start from
        :type ref_start: str

        :param ref_end: the commit ref to end
        :type ref_end: str

        :param max_refs: the maximum number of commits to return
        :type max_refs: int - defaults to 50

        :returns: a list with the commits details
        :rtype: list

        :raises RetrieverError: when the range was not found in the
        retrieved commits
        """

        limit = 10

        phid_start = self.get_phids_for_objects(
            [self.get_commit_name(self.repo_name, ref_start)]
        )['result'].values()[0]['phid']
        phid_end = self.get_phids_for_objects(
            [self.get_commit_name(self.repo_name, ref_end)]
        )['result'].values()[0]['phid']

        while limit < max_refs:
            resp = self.get_recent_commits(number=limit)
            if phid_start in resp and phid_end in resp:
                return OrderedDict(
                    islice(resp.viewitems(), resp.keys().index(phid_end),
                           resp.keys().index(phid_start)))
        raise RetrieverError(
            "Range could not be found in the {} most recent commits".format(
                max_refs))
