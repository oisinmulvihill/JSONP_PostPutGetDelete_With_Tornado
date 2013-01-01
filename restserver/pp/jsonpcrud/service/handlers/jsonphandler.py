# -*- coding: utf-8 -*-
"""
This provides request handler functionality all other handlers will use.

Oisin Mulvihill
2012-12-18T11:15:09

"""
import json
import logging
import traceback

import tornado.ioloop
import tornado.web

from ...service.jquery_unparam import jquery_unparam


def to_utf8(text):
    """Convert the given text from unicode.

    This will pass through unchanged if its not unicode.

    :returns: A utf-8 encoded string.

    """
    if isinstance(text, unicode):
        text = text.encode("utf-8")

    return text


class JSONPHandler(tornado.web.RequestHandler):
    """The JSONP Handler with the extra magic to allow GET, POST, PUT,
    DELETE, etc requests.

    """
    log = logging.getLogger("%s.%s" % (__name__, "JSONPHandler"))

    def __init__(self, *args, **kwargs):
        super(JSONPHandler, self).__init__(*args, **kwargs)

        # Allow JSONP and other to exploit X-HTTP-Method-Override.
        self.json_data = ""
        request = self.request
        query = request.query
        query_data = jquery_unparam(query)
        body = request.body

        # Recover JSON body if the correct content type header is set.
        if request.headers.get("Content-Type") == "application/json":
            try:
                if body:
                    self.json_data = json.loads(body)

            except ValueError:
                msg = "prepare: decode JSON Body failed! <%s>" % body
                self.log.exception(msg)

        # Super non standard! JSONP can't do anything other then GET. This is
        # due to how it works under the covers. No header can be set. I'm going
        # to look inside the request arguments for the __headers__ object. This
        # can then provide "X-HTTP-Method-Override". This is then used to set
        # the intended HTTP method. Other headers could be provided.
        #
        elif "__headers__" in query_data:
            internal = query_data["__headers__"]
            if internal:
                # Set the JSON body to this data minus the internal dict. Down
                # stream doesn't need to know about this.
                query_data.pop("__headers__")
                self.json_data = query_data

                # Set the 'real' request method which will in turn trigger the
                # correct get/post/put/delete/etc method call:
                #
                method = internal.get("X-HTTP-Method-Override")
                if method:
                    request.method = method

        # This is a more "standard" approach to support GET/etc calls with this
        # header. Flash/Actionscript has to use this header to indicate the
        # actual method to use. It only suport GET/POST.
        #
        if 'X-HTTP-Method-Override' in request.headers:
            request.method = request.headers['X-HTTP-Method-Override']
            self.log.debug("X-HTTP-Method-Override <{}>".format(
                request.method
            ))

    def write_error(self, error_code, message=None, **kwargs):
        """Override the error writing function to output in JSON format.

        :param error_code: HTTP Error code.
        :param message: Error message to ouput.

        """
        msg = None
        ret = dict(error="", trace="", code=error_code)

        if 'exc_info' in kwargs:
            error, detail, tb = kwargs['exc_info']
            if error.__name__ == "HTTPException":
                # Set the error code properly for deliberate REST / HTTP error
                # codes raised from handlers.
                #
                ret['error'] = to_utf8(detail.args[1])
                ret['code'] = detail.args[0]

            else:
                # Unknown exception, roll with it:
                ret['code'] = 500
                ret['error'] = to_utf8("{0}".format(detail))
                msg = "".join(traceback.format_tb(tb))
                ret['trace'] = to_utf8(msg)

        # Log the error
        if not msg:
            msg = "%(error)s %(code)s %(trace)s" % ret

        self.log.error(msg)

        # Output the error
        self.log.debug("setting error code <%d>" % ret['code'])
        self.set_status(ret['code'])

        # Generate the error body:
        self.write(ret)

    def write(self, data):
        """Implement JSONP Support in the default write."""
        if isinstance(data, dict):
            reqid = self.get_argument("reqid", False)
            if reqid:
                data['reqid'] = reqid
            data = json.dumps(data)
            self.set_header("Content-Type", "application/json; charset=UTF-8")

        callback = self.get_argument("callback", False)
        if callback:
            data = "%s(%s)" % (callback, str(data))

        super(JSONPHandler, self).write(data)
