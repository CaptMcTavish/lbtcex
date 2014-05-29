import functools
import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings

import requests

logger = logging.getLogger(__name__)


def api_token_required(f):
    @functools.wraps(f)
    @login_required
    def requirer(request, *args, **kwargs):
        if not request.user.profile.access_token:
            return render(request, "client/access_token_needed.html")
        return f(request, *args, **kwargs)
    return requirer

def catch_expired_token_and_retry(f):
    """Tokens expire rather quickly, but we generally have a refresh token
    to get new ones as necessary.

    Try to get a new token and retry a invalid-token-failed call once.

    """

    @functools.wraps(f)
    def wrapper(request, *args, **kwargs):
        resp = f(request, *args, **kwargs)

        resp_json = resp.json()

        if "error" in resp_json and resp_json["error"]["error_code"] == 3:
            # expired/invalid token, try to get a new one with our refresh token
            logger.info("Invalid access token, trying to get a new one")

            results = requests.post(
                settings.LBTC_URL + "/oauth2/access_token/",
                data={"grant_type": "refresh_token",
                      "client_id": settings.LBTC_CLIENT_ID,
                      "client_secret": settings.LBTC_CLIENT_SECRET,
                      "refresh_token": request.user.profile.access_token_refresh_token,})

            if results.status_code != 200:
                # just return the original error
                return resp

            request.user.profile.set_access_token(**results.json())
            request.user.profile.save()

            return f(request, *args, **kwargs)

        return resp

    return wrapper

@catch_expired_token_and_retry
def api_get(request, path, params=None):
    headers = {"Authorization": "Bearer " + request.user.profile.access_token}

    if not params: params = {}
    params.update(access_token=request.user.profile.access_token)

    return requests.get(settings.LBTC_URL + path, params=params, headers=headers)

@catch_expired_token_and_retry
def api_post(request, path, data=None):
    headers = {"Authorization": "Bearer " + request.user.profile.access_token}

    if not data: data = {}
    data.update(access_token=request.user.profile.access_token)

    return requests.post(settings.LBTC_URL + path, data=data, headers=headers)
