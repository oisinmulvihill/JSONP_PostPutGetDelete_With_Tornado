# -*- coding: utf-8 -*-
"""
The Tornado REST Service.

Oisin Mulvihill
2012-12-18T11:15:09

"""
import pprint
import logging

import tornado.ioloop
import tornado.web

from pp.jsonpcrud.service.handlers import ping
from pp.jsonpcrud.service.handlers import restcrud
from pp.jsonpcrud.service.handlers import catchallhandler


def generate_urlspace():
    """This generates the URLS passed to tornado.web.Application(...)

    :returns: List of urls.

    """
    URLS = []

    # The complete map of supported URLs. Each module will have its own URLS
    # close to the definition of the Handlers it provides. This could probably
    # done more automatically later:

    URLS.extend(ping.URLS)
    URLS.extend(restcrud.URLS)

    # comes last: catch all unhandled URLS giving 404:
    URLS.extend(catchallhandler.URLS)

    return URLS


def tornado_main(cfg, options={}):
    """Create the tornado app with given config and run forever.

    :param cfg: This is a dict of fields from the configuration.

    E.g.::

        cfg = dict(
            # default:
            port=18123
        )

    """
    log = logging.getLogger("%s.tornado_main" % __name__)

    port = int(cfg.get('port', 18123))
    interface = cfg.get('interface', '0.0.0.0')

    urls = generate_urlspace()
    log.debug("URL Space:\n%s" % pprint.pformat(urls))

    application = tornado.web.Application(urls)
    application.listen(port, address=interface)
    log.info("Running: port <%d>." % port)
    tornado.ioloop.IOLoop.instance().start()
