from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from vnfs.models import Vnf, Operator
import math


class Area(models.Model):
    name = models.CharField(max_length=120)
    latitude = models.CharField(max_length=120, default='41.275621')
    longitude = models.CharField(max_length=120, default='1.986591')
    description = models.TextField(default='description')
    file = models.FileField(null=True, blank=True, upload_to='btss/')
    price = models.FloatField(null=True, blank=True, default=0)
    forecast = models.CharField(max_length=500, null=True, blank=True)
    rb_offer = models.CharField(max_length=500, null=True, blank=True,
                                default='[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]')
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name

    def get_absolut_url(self):
        return reverse("scenarios:area_detail", kwargs={"id": self.id})

    def get_bts(self):
        bts = self.bts.all()
        return bts

    def get_desc(self):
        return self.description

    def static_deploy(self):
        deploy = self.forecast[1:].rstrip(']').split(',')[:-1]
        deploy = [int(x) for x in deploy]
        item = max(deploy, key=lambda x: x)
        array = "["
        for i in range(24):
            array += str(item) + ","
        array = array.rstrip(',')
        array += "]"
        return array

    class Meta:
        ordering = ["-timestamp", "-update"]


class Bts(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=120, null=True, blank=True)
    ip = models.CharField(max_length=120)
    lat = models.CharField(max_length=120)
    longi = models.CharField(max_length=120)
    radio = models.IntegerField(null=True, blank=True)
    neighbor = models.CharField(max_length=500, null=True, blank=True)
    BW = models.CharField(max_length=500, null=True, blank=True)
    freCs = models.CharField(max_length=500, null=True, blank=True, default='')
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name

    def get_lat(self):
        return self.lat

    def get_ip(self):
        return self.ip

    def get_longi(self):
        return self.longi

    def start(self):
        return self.BW.split('-')[0]

    def max_dist(self, pt, f):
        """pt in dBm and f in MHz"""
        f = f / 1000000  # MHz
        d = 10 ** ((pt + 107 - 20 * math.log10(f) - 32.44) / 20)

        return d

    def propagation(self, d, f, way):
        if way == 'dl':
            pmin = -107  # dBm
        elif way == 'ul':
            pmin = -123.4  # dBm

        f = f / 1000000  # MHz
        pt = pmin + 20 * math.log10(d) + 20 * math.log10(f) + 32.44
        return pt

    class Meta:
        ordering = ["-timestamp", "-update"]


class OArea(models.Model):
    name = models.CharField(max_length=120, default='EETAC')
    propietario = models.ForeignKey(Operator, on_delete=models.CASCADE, null=True, blank=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True, blank=True)
    price = models.FloatField(null=True, blank=True, default=0)
    forecast = models.CharField(max_length=500, null=True, blank=True,
                                default='[17000000,14000000,11000000,9000000,7000000,8000000,9500000,12000000,14000000,3000000,3500000,3400000,5500000,3400000,3450000,3460000,3470000,3300000,6000000,11000000,18000000,21000000,20500000,19500000]')
    rb_offer = models.CharField(max_length=500, null=True, blank=True,
                                default='[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]')
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name

    def get_absolut_url(self):
        return reverse("scenarios:area_detail", kwargs={"id": self.id})

    def static_deploy(self):
        deploy = self.forecast[1:].rstrip(']').split(',')[:-1]
        deploy = [int(x) for x in deploy]
        item = max(deploy, key=lambda x: x)
        array = "["
        for i in range(24):
            array += str(item) + ","
        array = array.rstrip(',')
        array += "]"
        return array
