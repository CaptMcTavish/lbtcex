import functools

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings

import requests


def api_token_required(f):
    @functools.wraps(f)
    @login_required
    def requirer(request, *args, **kwargs):
        if not request.user.profile.access_token:
            return render(request, "client/access_token_needed.html")
        return f(request, *args, **kwargs)
    return requirer

def api_get(request, path, params=None):
    p = {"access_token": request.user.profile.access_token}
    if params is not None:
        p.update(params)

    return requests.get(settings.LBTC_URL + path, params=p)

def api_post(request, path, data=None):
    d = {"access_token": request.user.profile.access_token}
    if data is not None:
        d.update(data)

    return requests.post(settings.LBTC_URL + path, data=d)
