from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse

class Operator(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    name = models.CharField(max_length=120)
    bandwidth = models.FloatField()
    mcs = models.FileField(null=True, blank=True,upload_to='settings/')
    colors = models.CharField(max_length=500,null=True, blank=True)
    end_nova=models.CharField(max_length=120,null=True, blank=True,default="http://147.83.188.226:5000/v2.0/")
    end_keystone=models.CharField(max_length=120,null=True, blank=True,default="http://147.83.188.226:5000/v2.0/")
    end_ceilometer=models.CharField(max_length=120,null=True, blank=True,default="http://147.83.188.226:8777")
    end_heat=models.CharField(max_length=120,null=True, blank=True,default="http://147.83.188.226:8004/v1/")

    def __unicode__(self):
		return self.name
