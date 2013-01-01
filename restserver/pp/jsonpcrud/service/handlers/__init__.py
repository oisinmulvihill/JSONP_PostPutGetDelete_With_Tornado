# -*- coding: utf-8 -*-
"""
The Tornado REST Service URL handlers.

Oisin Mulvihill
2012-08-22

"""
import time

def now():
    return time.asctime()


def data(request):
    """Strip out JSONP/JQuery stuff we don't need."""
    d = request.json_data if request.json_data else {}
    if 'callback' in d:
        d.pop('callback')
    if '_' in d:
        d.pop('_')
    return d
