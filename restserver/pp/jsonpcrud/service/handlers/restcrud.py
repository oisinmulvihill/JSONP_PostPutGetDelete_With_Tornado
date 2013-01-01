# -*- coding: utf-8 -*-
"""
This provides a URL you can call to check if the service is present
and its current version.

Oisin Mulvihill
2012-12-18T11:15:09

"""
import logging

from pp.jsonpcrud.service.handlers import now
from pp.jsonpcrud.service.handlers import data
from pp.jsonpcrud.service.handlers.jsonphandler import JSONPHandler


class RESTCRUDHandler(JSONPHandler):

    log = logging.getLogger("%s.RESTCRUDHandler" % __name__)

    def post(self):
        """Create."""
        self.log.info("POST data: {0}".format(data(self)))
        self.write(dict(msg="POST: OK", received=now()))

    def get(self):
        """Recover."""
        self.log.info("GET data: {0}".format(data(self)))
        self.write(dict(msg="GET: OK", received=now()))

    def put(self):
        """Update."""
        self.log.info("PUT data: {0}".format(data(self)))
        self.write(dict(msg="PUT: OK", received=now()))

    def delete(self):
        """Delete."""
        self.log.info("DELETE data: {0}".format(data(self)))
        self.write(dict(msg="DELETE: OK", received=now()))


URLS = [
    (r"/$", RESTCRUDHandler),
]
