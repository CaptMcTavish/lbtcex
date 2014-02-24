from django.conf.urls import *

urlpatterns = patterns('',
    url(r'^$', 'lbtcex.main.views.index', name="index"),
)
