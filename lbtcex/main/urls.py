from django.conf.urls import *

urlpatterns = patterns('',
    url(r'^$', 'lbtcex.main.views.index', name="index"),
    url(r'^call/$', 'lbtcex.main.views.api_call', name="api_call")
)
