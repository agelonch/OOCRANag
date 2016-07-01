from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse

class Operator(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    name = models.CharField(max_length=120)
    bandwidth = models.FloatField()
    mcs = models.FileField(null=True, blank=True,upload_to='settings/')
    end_nova=models.CharField(max_length=120,null=True, blank=True)
    end_keystone=models.CharField(max_length=120,null=True, blank=True)
    end_ceilometer=models.CharField(max_length=120,null=True, blank=True)
    end_heat=models.CharField(max_length=120,null=True, blank=True)

    def __unicode__(self):
		return self.name
