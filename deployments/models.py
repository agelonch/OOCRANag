from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from scenarios.models import OArea
from vnfs.models import Operator
from vnfs.models import Vnf, Operator
from scenarios.models import Bts


class Deployment(models.Model):
    propietario = models.ForeignKey(Operator, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=120)
    area = models.ForeignKey(OArea, null=True, blank=True)
    file = models.FileField(null=True, blank=True, upload_to='deployments/')
    start = models.TimeField(null=True, blank=True)
    stop = models.TimeField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True, default=0)
    rb = models.IntegerField(null=True, blank=True, default=0)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name

    '''def cpu(self):
		total = 0
		nvfs= self.nvfs.all()
		for nvf in nvfs:
			total=total+nvf.vnf.cpu
		return total

	def ram(self):
		total = 0
		nvfs= self.nvfs.all()
		for nvf in nvfs:
			total=total+nvf.vnf.ram
		return total'''

    def get_scenario(self):
        return self.area.name

    '''def get_nvfs(self):
		return self.nvfs.all()'''

    def get_absolut_url(self):
        return reverse("deployments:detail", kwargs={"id": self.id})

    class Meta:
        ordering = ["-timestamp", "-update"]


class Nvf(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE, null=True, blank=True)
    deploy = models.ForeignKey(Deployment, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    type = models.CharField(max_length=20, null=True, blank=True)
    load = models.CharField(max_length=400, null=True, blank=True)
    # Downlink
    freC_DL = models.IntegerField(null=True, blank=True)
    color_DL = models.CharField(max_length=20, null=True, blank=True, default="#AA0000")
    BW_DL = models.IntegerField(null=True, blank=True)
    rb = models.IntegerField(null=True, blank=True)
    Pt = models.FloatField(null=True, blank=True)
    # Uplink
    freC_UL = models.IntegerField(null=True, blank=True)
    color_UL = models.CharField(max_length=20, null=True, blank=True)
    BW_UL = models.IntegerField(null=True, blank=True)
    #
    vnf = models.ForeignKey(Vnf, null=True, blank=True)
    radio = models.CharField(max_length=120, null=True, blank=True, default=0)
    bts = models.ForeignKey(Bts, null=True, blank=True)
    static_labels = models.CharField(max_length=400, null=True, blank=True)
    static_cpu = models.CharField(max_length=400, null=True, blank=True)
    static_ram = models.CharField(max_length=400, null=True, blank=True)
    static_net = models.CharField(max_length=400, null=True, blank=True)
    users = models.IntegerField(null=True, blank=True, default=0)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name.split('-')[1]

    def get_absolut_url(self):
        return reverse("deployments:nvf_detail", kwargs={"id": self.id})

    def get_name(self):
        return self.name.split('-')[1]

    class Meta:
        ordering = ["-timestamp", "-update"]


class Channel(models.Model):
    propietario = models.ForeignKey(Operator, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=120, default="AWGN")
    deploy = models.ForeignKey(Deployment, on_delete=models.CASCADE, null=True, blank=True)
    ip = models.CharField(max_length=20, null=True, blank=True)
    snr = models.FloatField(null=True, blank=True)
    vnf = models.ForeignKey(Vnf, on_delete=models.CASCADE, null=True, blank=True)

    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name

    def get_absolut_url(self):
        return reverse("deployments:channel_detail", kwargs={"id": self.id})
