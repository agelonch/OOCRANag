"""trydjango19 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from .views import (
	network_list,
	network_create,
	#nvf_detail,
	#nvf_edit,
	network_delete,
	)

urlpatterns = [
	url(r'^$', network_list, name="list"),
    url(r'^create/$', network_create),
    #url(r'^(?P<id>\d+)/$', nvf_detail, name='detail'),
    #url(r'^(?P<id>\d+)/edit/$', nvf_edit, name="edit"),
    url(r'^(?P<id>\d+)/delete/$', network_delete, name="delete"),
]