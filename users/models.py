from __future__ import unicode_literals
from vnfs.models import Operator
from deployments.models import Deployment, Nvf
from django.db import models


class Client(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=120, null=True, blank=True)
    pt_dl = models.FloatField(null=True, blank=True)
    pt_ul = models.FloatField(null=True, blank=True)
    lat = models.CharField(max_length=120, null=True, blank=True)
    longi = models.CharField(max_length=120, null=True, blank=True)
    dist = models.CharField(max_length=120, null=True, blank=True)
    deploy = models.ForeignKey(Deployment, null=True, blank=True)
    rb = models.IntegerField(null=True, blank=True)
    nvf = models.ForeignKey(Nvf, null=True, blank=True)
    mcs = models.IntegerField(null=True, blank=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name.split('-')[1]

    def get_name(self):
        return self.name.split('-')[1]

    def get_lat(self):
        return self.lat

    def get_longi(self):
        return self.longi

    class Meta:
        ordering = ["-timestamp", "-update"]

