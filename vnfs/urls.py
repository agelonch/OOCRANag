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
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView

from .views import (
	vnf_list,
	vnf_create,
	vnf_detail,
	vnf_delete,
)

urlpatterns = [
	url(r'^$', vnf_list, name="list"),
    url(r'^create/$', vnf_create),
    url(r'^(?P<id>\d+)/$', vnf_detail, name='detail'),
    url(r'^(?P<id>\d+)/delete/$', vnf_delete),
]