# -*- coding: utf-8 -*-
"""
This provides a URL you can call to check if the service is present
and its current version.

Oisin Mulvihill
2012-12-18T11:15:09

"""
import logging
import pkg_resources

from pp.jsonpcrud.service.handlers.jsonphandler import JSONPHandler


class PingHandler(JSONPHandler):

    log = logging.getLogger("%s.PingHandler" % __name__)

    def get(self):
        """This will return the package name and version response.

        :returns: a gen_response(...) wrapped dict.

        E.g.::

            {
                'name': 'pp-jsonpcrud-service',
                'version': 'x.y.z',
            }

        """
        pkg = pkg_resources.get_distribution("pp-jsonpcrud-service")

        rc = {
            'name': 'pp-jsonpcrud-service',
            'version': pkg.version,
        }

        self.log.debug("ping! returning <%s>" % rc)
        self.write(rc)


URLS = [
    (r"/ping", PingHandler),
]
