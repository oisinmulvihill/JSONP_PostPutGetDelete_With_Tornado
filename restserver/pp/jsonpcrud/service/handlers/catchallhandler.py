# -*- coding: utf-8 -*-
"""

Oisin Mulvihill
2012-12-18T11:15:09

"""
import logging

from pp.jsonpcrud.service.handlers.jsonphandler import JSONPHandler


class CatchAllHandler(JSONPHandler):

    log = logging.getLogger("%s.CatchAllHandler" % __name__)

    def notfound(self):
        msg = "Not found {0}".format(self.request.path)
        ret = dict(error="", trace="", code=404)
        self.log.error(msg)
        self.set_status(ret['code'])
        self.write(ret)

    def get(self, *args, **kwargs):
        self.notfound()

    def post(self, *args, **kwargs):
        self.notfound()

    def put(self, *args, **kwargs):
        self.notfound()

    def delete(self, *args, **kwargs):
        self.notfound()

    def options(self, *args, **kwargs):
        self.notfound()

    def head(self, *args, **kwargs):
        self.notfound()

    def patch(self, *args, **kwargs):
        self.notfound()

URLS = [
    (r".*", CatchAllHandler),
]
