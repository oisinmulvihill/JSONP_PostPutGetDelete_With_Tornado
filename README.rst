JSONP POST, PUT, GET, DELETE With Tornado
=========================================

.. contents::


The Problem
-----------

Internet browsers restrictions prevent you from doing AJAX calls to another
domain. You are restricted to only calling your own domain. JSONP is a way to
get around this. It works by exploiting the fact the script tags can source
code on other domains. Because of this JSONP can only issue GET requests. It
is not possible to change the headers of a request which you might also want to
do. This is a problem if you work with web based REST_ services. These usually
use GET, POST, PUT, DELETE which change the meaning of the request.


A Solution
----------

The is no way a JSONP only client can do any request other then a GET. My
solution is to add a "hint" in the client side and then get the server to look
out for this.



Running the demo
================

Run the server and client. The connect your browser to http://localhost:8000
to see the client side UI.


Client
======

 * Change into jsonpclient.

 * Run the simple web server hosting the JS client app::

    $./serve.sh
    Press Control-C to exit.
    Serving HTTP on 0.0.0.0 port 8000 ...

 * In your browser open the client side address http://localhost:8000


Server
======

This provides a Tornado based REST service to demonstrate JSONP and support
for GET, POST, PUT, DELETE.

Running
-------

 * Change into pp-jsonpcrud-service.

 * Set up the pp-jsonpcrud-service package in your environment through setuptools::

    python setup.py develop

 * Run the service (Control-C exits)::

    restservice
    DEBUG [root][MainThread] config: recovering config from <config.ini>
    DEBUG [pp.jsonpcrud.service.appmain.tornado_main][MainThread] URL Space:
    [('/ping', <class 'pp.jsonpcrud.service.handlers.ping.PingHandler'>),
     ('/$', <class 'pp.jsonpcrud.service.handlers.restcrud.CRUDHandler'>),
     ('.*',
      <class 'pp.jsonpcrud.service.handlers.catchallhandler.CatchAllHandler'>)]
    INFO  [pp.jsonpcrud.service.appmain.tornado_main][MainThread] Running: port <18123>.

When the service is running you can do standard REST calls using curl. For
example::

    # Check the version page:
    curl http://localhost:18123/ping | python -m json.tool
    {
        "name": "pp-jsonpcrud-service",
        "version": "1.0.0"
    }

    # Standard GET/POST/etc calls:
    curl http://localhost:18123/ | python -m json.tool
    {
        "msg": "GET: OK",
        "received": "Thu Dec 20 19:53:27 2012"
    }

    curl -H "Content-Type: application/json" -X PUT -d '{"a": 1}' http://localhost:18123/ | python -m json.tool
    {
        "msg": "PUT: OK",
        "received": "Thu Dec 20 19:53:27 2012"
    }

    curl -H "Content-Type: application/json" -X DELETE -d '{"a": 1}' http://localhost:18123/ | python -m json.tool
    {
        "msg": "DELETE: OK",
        "received": "Thu Dec 20 19:53:27 2012"
    }


Testing
-------

 * Change into pp-jsonpcrud-service.

 * Set up the pp-jsonpcrud-service package in your environment through setuptools::

    python setup.py develop

 * Run all tests::

    python runtests.py -s


.. _JSONP: http://en.wikipedia.org/wiki/JSONP
.. _REST: http://en.wikipedia.org/wiki/REST
