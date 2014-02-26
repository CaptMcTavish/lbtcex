import os

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings

import requests

@login_required
def start_authorize(request):
    state_token = os.urandom(16).encode("hex")
    request.session["state_token"] = state_token

    return render(request,
                  "client/start_authorize.html",
                  {"client_id": settings.LBTC_CLIENT_ID,
                   "state_token": state_token,
                   "lbtc_url": settings.LBTC_URL})

@login_required
def get_auth_code(request):
    code = request.GET.get("code")
    state = request.GET.get("state")

    if not code or not state:
        return render(request, "client/no_auth_code.html")

    if "state_token" not in request.session:
        return render(request, "client/session_fail.html")

    if state != request.session["state_token"]:
        return render(request, "client/unauthorized_get.html")

    results = requests.post(
        settings.LBTC_URL + "/oauth2/access_token/",
        data={"code": code,
              "grant_type": "authorization_code",
              "client_id": settings.LBTC_CLIENT_ID,
              "client_secret": settings.LBTC_CLIENT_SECRET})

    if results.status_code != 200:
        return render(request, "client/failed_token_get.html", {
            "results": results,
            "code": code
        })

    access_token_info = results.json()

    request.user.profile.set_access_token(**access_token_info)
    request.user.profile.save()

    return render(request, "client/authorization_success.html")
