import json

from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm

from registration.forms import RegistrationForm

from lbtcex.client.utils import api_token_required, api_get, api_post
from lbtcex.main.forms import ApiCallForm


def index(request):
    if request.user.is_authenticated():
        return render(request, "dashboard.html")
    else:
        return render(
            request,
            "index.html",
            {
                "login_form": AuthenticationForm(),
                "registration_form": RegistrationForm(),
            }
        )

@api_token_required
def api_call(request):
    if request.method == "POST":
        opts = ApiCallForm(request.POST)
        if opts.is_valid():
            if opts.cleaned_data["data"]:
                data = json.loads(opts.cleaned_data["data"])
            else:
                data = {}

            if opts.cleaned_data["method"] == "POST":
                result = api_post(request,
                                  opts.cleaned_data["path"],
                                  data)
            else:
                result = api_get(request,
                                 opts.cleaned_data["path"],
                                 data)

            return render(request,
                          "api_call.html",
                          {"form": opts,
                           "got_result": True,
                           "result": result,
                           "result_pretty_json": json.dumps(result.json(), indent=4)})
    else:
        opts = ApiCallForm()

    return render(request, "api_call.html", {"form": opts})
