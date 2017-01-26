import abc
import json

from collections import OrderedDict
from urllib import urlencode
from urllib2 import Request, urlopen

from django.conf import settings

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

        :returns: :class:`urllib2.Request`
        """

        data = kwargs.get('data') or dict()
        headers = kwargs.get('headers') or dict()

        (data, headers) = self.authorize_request(data=data, headers=headers)
        url = self.api_url.strip('/') + '/' + endpoint

        return Request(url, urlencode(data, doseq=True), headers)


class PhabricatorRetriever(ProjectStatusRetriever):
    """
    Implement a `ProjectStatusRetriever` for a phabricator hosting service
    """

    @staticmethod
    def get_api_url(url):
        """
        Parses a phabricator repository URL (https) and returns the
        api url

        :param url: The phabricator repository url
        :type url: str

        :returns str: The phabricator api url
        """
        # remove 'https://', split on ('/'), keep the first part (the host),
        # add 'https://' again
        return 'https://' + url.replace('https://', '').split('/')[0] + '/api'

    @staticmethod
    def get_repo_name(url):
        """
        Parses a phabricator repository URL (https) and returns the
        repository name

        :param url: The phabricator repository url
        :type url: str

        :returns str: The phabricator repository name
        """
        # remove 'https://', split on ('/'), keep the semi-final part
        return 'r' + url.replace('https://', '').split('/')[-2]


    def __init__(
            self, url, api_token=getattr(settings, 'PHABRICATOR_API_TOKEN')):
        """
        Initializes an instance calling `super` with the required
        parameters

        :param url: a phabricator repository url (https only)
        :type url: str

        :param api_token: the phabricator API (Conduit) token
        :type api_token: str

        :returns: None
        """
        self.repo_phid = ''
        self.repo_name = ''
        super(PhabricatorRetriever, self).__init__(
            self.get_api_url(url), {'api.token': api_token})
        self.set_repo(url)

    def set_repo(self, url):
        """
        Initializes an instance to work on a specific repo.

        :param url: A phabricator repository url
        :type url: str

        :returns: None
        """
        self.repo_name = self.get_repo_name(url)
        self.repo_phid = self.get_phids_for_objects(
            [self.repo_name])['result'][self.repo_name]['phid']

    def authorize_request(self, **kwargs):
        """
        Add `self.api_auth` string to request data to authorize it

        :returns: tuple
        """
        data = dict(kwargs['data'])
        data.update(self.api_auth)
        return (data, kwargs['headers'])

    def get_phids_for_objects(self, names):
        """
        Returns `phid`s of the given "name"s

        :param name: The "name"s of the objects for which a `phid` should
        be retrieved
        :type name: list

        :returns: list - The objects' `phid`s
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

        :returns: list - a list with the commits details
        """

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
