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
from .forms import LoginForm

from .views import (
	deployment_list,
	deployment_create,
	deployment_detail,
	deployment_edit,
	deployment_delete,
    nvf_detail,
    login,
    canals_list,
    autodeploy,
    catalog,
    add_catalog,
    del_catalog,
	)

urlpatterns = [
	url(r'^$', deployment_list, name="list"),
    url(r'^(?P<id>\d+)/$', deployment_detail, name='detail'),
    url(r'^(?P<id>\d+)/edit/$', deployment_edit, name='edit'),
    url(r'^(?P<id>\d+)/delete/$', deployment_delete, name='delete'),
    url(r'^(?P<id>\d+)/create/$', deployment_create, name='create'),
    url(r'^(?P<id>\d+)/autodeploy/$', autodeploy, name='autodeploy'),
    url(r'^(?P<id>\d+)/catalog/add_catalog/$', add_catalog, name='catalog_create'),
    url(r'^(?P<id>\d+)/catalog/delete/(?P<id_deploy>\d+)', del_catalog, name='catalog_delete'),
    url(r'^(?P<id>\d+)/catalog/$', catalog, name='catalog'),
    url(r'^nvf/(?P<id>\d+)/$', nvf_detail, name='nvf_detail'),
    url(r'^canals/$', canals_list, name='canals'),
]