from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView

from .views import (
	settings,
	mcs,
)

urlpatterns = [
	url(r'^$', settings, name="settings"),
	url(r'^mcs/$', mcs, name='mcs'),
    #url(r'^settings/$', settings,name="settings"),
    #url(r'^(?P<id>\d+)/$', vnf_detail, name='detail'),
    #url(r'^(?P<id>\d+)/delete/$', vnf_delete),
]