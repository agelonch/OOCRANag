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
    scenarios_list,
    area_create,
    area_detail,
    scenario_delete,
)

urlpatterns = [
    url(r'^$', scenarios_list, name="list"),
    url(r'^create_area/$', area_create, name='area_create'),
    url(r'^areas/(?P<id>\d+)/$', area_detail, name='area_detail'),
    # url(r'^(?P<id>\d+)/edit/$', vnf_edit, name='edit'),
    url(r'^(?P<id>\d+)/delete/$', scenario_delete, name="delete"),



]
