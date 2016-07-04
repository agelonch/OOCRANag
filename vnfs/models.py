from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from operators.models import Operator

class Vnf(models.Model):
	operador = models.ForeignKey(Operator, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=120, default="TX_LTE")
	modules = models.FileField(null=True, blank=True,upload_to='vnfs/modules/')
	yaml = models.FileField(null=True, blank=True,upload_to='vnfs/yaml/')
	description = models.TextField(null=True, blank=True, default ="SDN code for launch pyshical layer LTE TX")
	cpu = models.IntegerField(null=True, blank=True)
	ram = models.IntegerField(null=True, blank=True)
	update = models.DateTimeField(auto_now=True,auto_now_add=False)
	script = models.TextField(null=True, blank=True, default="cd /home/nodea/DADES_TX/srsLTE/build/srslte/examples\n ./pdsch_enodeb_multiUser -l 0.3 -g 40.0 -p 6 -i rfc793.txt -o prova.txt")
	image = models.CharField(max_length=120, null=True, blank=True, default="TX_LTE")
	timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)

	def __unicode__(self):
		return self.name

	def get_absolut_url(self):
		return reverse("vnfs:detail",kwargs={"id":self.id})

	class Meta:
		ordering = ["-timestamp","-update"]



