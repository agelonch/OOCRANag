from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from operators.models import Operator

class Vnf(models.Model):
	operador = models.ForeignKey(Operator, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=120)
	modules = models.FileField(null=True, blank=True,upload_to='vnfs/modules/')
	yaml = models.FileField(null=True, blank=True,upload_to='vnfs/yaml/')
	description = models.TextField(null=True, blank=True)
	cpu = models.IntegerField(null=True, blank=True)
	ram = models.IntegerField(null=True, blank=True)
	update = models.DateTimeField(auto_now=True,auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)

	def __unicode__(self):
		return self.name

	def get_absolut_url(self):
		return reverse("vnfs:detail",kwargs={"id":self.id})

	class Meta:
		ordering = ["-timestamp","-update"]



