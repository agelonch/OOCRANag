from __future__ import unicode_literals
from vnfs.models import Operator
from django.db import models
from django.core.urlresolvers import reverse

class Controller(models.Model):
	operator = models.ForeignKey(Operator, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=20)
	cluster = models.CharField(null=True, blank=True, max_length=20)
	vnc = models.CharField(null=True, blank=True, max_length=200)
	network = models.CharField(max_length=20, null=True, blank=True)
	update = models.DateTimeField(auto_now=True,auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)

	def __unicode__(self):
		return self.name

	def get_absolut_url(self):
		return reverse("networks:detail",kwargs={"id":self.id})

	class Meta:
		ordering = ["-timestamp","-update"]