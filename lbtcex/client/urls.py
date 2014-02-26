from django.conf.urls import *

urlpatterns = patterns('lbtcex.client.views',
    url("^$", "start_authorize", name="start_authorize"),
    url("^success/$", "get_auth_code", name="get_auth_code"),
)
