from math import radians, cos, sin, asin, sqrt
import numpy as np
import random
from django.shortcuts import get_object_or_404
from vnfs.models import Vnf, Operator
from scenarios.models import Bts, Area
from deployments.models import Deployment, Nvf
from users.models import Client
from twisted.internet import task
from twisted.internet import reactor
import threading, time
from aloeoCLI.VNFM.deployments.deployments import create
from .authentication import auth
from .orchestration import planification_DL, planification_UL, price

def my_scheduled_job():
  deploy = get_object_or_404(Deployment, stop=time.strftime("%H:00:00"))
  nvfs = Nvf.objects.filter(deploy__name=deploy.name)
  for nvf in nvfs:
		bts = get_object_or_404(Bts, ip=nvf.bts.ip)
		lista = bts.freCs.split('/')
		lista.remove(str(nvf.freC_DL-nvf.BW_DL/2)+"-"+str(nvf.freC_DL+nvf.BW_DL/2))
		lista.remove(str(nvf.freC_UL-nvf.BW_UL/2)+"-"+str(nvf.freC_UL+nvf.BW_UL/2))
		bts.freCs= '/'.join(lista)
		bts.save()

  deploy.delete()


def auto_delete_deploy_job():
	deploys = Deployment.objects.filter(propietario__name="operator1").filter(start__isnull=False)
	    
	for deploy in deploys:
		plan = str(deploy.area.rb_offer)[1:-1].split(',')

		nvfs = Nvf.objects.filter(deploy__name=plan[int(time.strftime("%H"))-1])
        for nvf in nvfs:
        	bts = get_object_or_404(Bts, ip = nvf.bts.ip)
        	if len(bts.freCs) is 0:
        		continue
        	else:
        		lista = bts.freCs.split('/')
        		lista.remove(str(nvf.freC_DL-nvf.BW_DL/2)+"-"+str(nvf.freC_DL+nvf.BW_DL/2))
        		lista.remove(str(nvf.freC_UL-nvf.BW_UL/2)+"-"+str(nvf.freC_UL+nvf.BW_UL/2))
        		bts.save()
        		nvf.freC_DL = 0
        		nvf.freC_UL = 0
        		nvf.radio = 0
        		nvf.save()
		

def auto_create_deploy_job():
	deploys = Deployment.objects.filter(propietario__name="operator1").filter(start__isnull=False)
	    
	for deploy in deploys:
		plan = str(deploy.area.rb_offer)[1:-1].split(',')
		nvfs = Nvf.objects.filter(deploy__name=plan[int(time.strftime("%H"))])
        for nvf in nvfs:
	        bts = get_object_or_404(Bts, ip = nvf.bts.ip)
	        bts.freCs = planification_DL(nvf, Bts.objects.filter(area__name="EETAC"))
	        bts.save()
	        bts.freCs = planification_UL(nvf, Bts.objects.all())
	        nvf.radio = nvf.bts.max_dist(nvf.Pt,nvf.freC_DL)          
	        deploy.rb += nvf.rb_offer
	        deploy.price = deploy.price + price(nvf, nvf.BW_DL, deploy)
	        bts.save()
	        nvf.save()
	        deploy.save()