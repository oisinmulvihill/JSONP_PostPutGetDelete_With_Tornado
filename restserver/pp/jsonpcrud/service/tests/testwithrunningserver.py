# -*- coding: utf-8 -*-
"""
Tests to verify the REST interface provided by a running test tornado instance.

Oisin Mulvihill
2012-12-18T11:15:09

"""
import unittest
import pkg_resources

from pp.jsonpcrud.service.tests import svrhelp


# -*- coding: utf-8 -*-
"""
This provides the REST classes used to access the User Service.

"""
import json
import logging
from urlparse import urljoin

import requests


class RESTAPI(object):
    """Client side REST lib helper for basic testing.
    """
    HEADERS = {
        'Content-Type': 'application/json'
    }

    def __init__(self, uri='http://localhost:18123'):
        """Set the URI of the REST Service.

        :param uri: The base address of the API Audience Service.

        """
        self.log = logging.getLogger('{}.Service'.format(__name__))
        self.uri = uri

    def ping(self):
        res = requests.get(urljoin(self.uri, 'ping'))
        res.raise_for_status()
        return json.loads(res.content)

    def do(self, method, **kwargs):
        """Wrapper around GET, POST, PUT, DELETE..."""
        d = {}
        if kwargs:
            d['data'] = kwargs

        res = getattr(requests, method)(
            self.uri,
            headers=self.HEADERS,
            **d
        )
        res.raise_for_status()
        return json.loads(res.content)


def setup_module():
    """Start the test app running on module set up and stop it
    running on teardown.

    """
    svrhelp.setup_module()

    # Create the db now the server is running in its own dir.
    #db.init(...)

teardown_module = svrhelp.teardown_module


class BasicTesting(unittest.TestCase):

    def setUp(self):
        # Set up the REST API client:
        self.api = RESTAPI(svrhelp.serviceapp.URI)

    def test_service(self):
        """Test the ping and basic REST get/post/put/delete etc.
        """
        report = self.api.ping()
        self.assertTrue("name" in report)
        self.assertTrue("version" in report)

        pkg = pkg_resources.get_distribution("pp-jsonpcrud-service")

        self.assertEquals(report['name'], 'pp-jsonpcrud-service')
        self.assertEquals(report['version'], pkg.version)

        rc = self.api.do("get")
        self.assertEquals(rc['msg'], "GET: OK")

        rc = self.api.do("post", a=1)
        self.assertEquals(rc['msg'], "POST: OK")

        rc = self.api.do("put", a=1)
        self.assertEquals(rc['msg'], "PUT: OK")

        rc = self.api.do("delete", a=1)
        self.assertEquals(rc['msg'], "DELETE: OK")
