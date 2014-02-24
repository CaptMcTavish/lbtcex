from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm

from registration.forms import RegistrationForm


# Create your views here.

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
