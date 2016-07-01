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

def optim(file):
    """
    Parser user characteristics
    """
    lista = []
    users = np.genfromtxt(file,dtype='str')
    
    for user in users:
        vm = {}
        vm['name'] = user.split(',')[0]
        vm['lat'] = user.split(',')[1]
        vm['long'] = user.split(',')[2]
        vm['bts'] = user.split(',')[3]
        vm['vnf'] = user.split(',')[4]
        vm['rb'] = user.split(',')[5]
        vm['mcs'] = user.split(',')[6]
        lista.append(vm)
        
    return lista

def distance(lon1, lat1, lon2, lat2):
    """
    Calculate distance between terminal and bts
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km*1000

def mcs(value,operator):
        mcs = operator.mcs
        i=0
        for row in mcs:
            row = row.split('\n')[0]
            if row.split(',')[0] == value:
                return row.split(',')[1] 
            i+=1