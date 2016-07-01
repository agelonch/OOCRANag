from django.conf.urls import url
from django.contrib import admin
#from .forms import LoginForm

from .views import (
	users_list,
	users_create,
	)

urlpatterns = [
	url(r'^$', users_list, name="list"),
    #url(r'^(?P<id>\d+)/$', users_detail, name='detail'),
    #url(r'^(?P<id>\d+)/edit/$', users_edit, name='edit'),
    #url(r'^(?P<id>\d+)/delete/$', users_delete, name='delete'),
    url(r'^create/$', users_create, name='create'),
]