from math import radians, cos, sin, asin, sqrt
import numpy as np
import random
import ast
from django.shortcuts import get_object_or_404
from vnfs.models import Vnf, Operator
from scenarios.models import Bts, Area


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

def price(nvf, spectre,deploy):
    price_spec = 0
    if spectre == 1400000:
        price_spec = 1.74
    if spectre == 3000000:
        price_spec = 200.0
    if spectre == 5000000:
        price_spec = 300.0
    if spectre == 10000000:
        price_spec = 400.0

    t = int(deploy.stop.strftime("%H")) - int(deploy.start.strftime("%H"))
    #price = (price_spec+nvf.vnf.ram*0.005+nvf.vnf.cpu*0.005)*t
    price = price_spec*t
         
    return float(price)

def rb_offer(rb,total,start,stop,operation):

    value = total[1:-1].split(',')

    for i in range(stop-start+1):
        if operation == "suma":
            value[start+i]=str(int(value[start+i])+int(rb))
        if operation == "resta":
            value[start+i]=str(int(value[start+i])-int(rb))
        
    valores= ','.join(value)
    return "["+valores+"]"

def mcs(value,operator):
        mcs = operator.mcs
        i=0
        for row in mcs:
            row = row.split('\n')[0]
            if row.split(',')[0] == value:
                return row.split(',')[1] 
            i+=1

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

def list_bs(file):
    """
    Parser user characteristics
    """
    lista = []
    btss = np.genfromtxt(file,dtype='str')

    for bts in btss:
        nvf = {}
        nvf['ip'] = bts.split(',')[0]
        nvf['vnf'] = bts.split(',')[1]
        nvf['rb'] = bts.split(',')[2]
        nvf['pt'] = bts.split(',')[3]
        nvf['type'] = bts.split(',')[4]
        nvf['channel'] = bts.split(',')[5]
        nvf['subs'] = bts.split(',')[6]
        lista.append(nvf)
        
    return lista

def rand_color():
    """
    Random color generator
    """
    r = lambda: random.randint(0,255)
    color = ('#%02X%02X%02X' % (r(),r(),r()))
    return color


def planification_DL(nvf,colors_op):

    start = nvf.bts.start()
    colors = ast.literal_eval(colors_op.colors)

    if nvf.BW_DL == 1400000:
        nvf.rb = 18000000
    if nvf.BW_DL == 3000000:
        nvf.rb = 36000000
    if nvf.BW_DL == 5000000:
        nvf.rb = 72000000
    if nvf.BW_DL == 10000000:
        nvf.rb = 150000000

    neigh = [ str(x) for x in nvf.bts.neighbor.split('/') ]
    frequencies = []
    for bts in neigh:
        bts = get_object_or_404(Bts, ip = bts)
        freqs = [str(x) for x in bts.freCs.split('/')]
        for frec in freqs:
            frequencies.append(frec)

    assigned = [ str(x) for x in nvf.bts.freCs.split('/') ]

    while (True):
        if not str(start)+'-'+str(int(start)+int(nvf.BW_DL)) in frequencies:
            if not str(start)+'-'+str(int(start)+int(nvf.BW_DL)) in assigned:
                nvf.bts.freCs = str(nvf.bts.freCs)+'/'+str(start)+'-'+str(int(start)+int(nvf.BW_DL))
                nvf.freC_DL = int(start)+int(nvf.BW_DL)/2
                break
            else:
                start = int(start)+int(nvf.BW_DL)
        else:
            start = int(start)+int(nvf.BW_DL)

    if colors.has_key(nvf.freC_DL):
        nvf.color_DL = colors[nvf.freC_DL]
    else:
        nvf.color_DL = rand_color()
        colors[nvf.freC_DL] = nvf.color_DL
        colors_op.colors = str(colors)

    nvf.save()
    bts.save()
    return nvf.bts.freCs
    

def planification_UL(nvf):
    start = int(nvf.bts.start())+20000000

    nvf.color_UL = rand_color() 
    neigh = [ str(x) for x in nvf.bts.neighbor.split('/') ]

    frequencies = []
    for bts in neigh:
        bts = get_object_or_404(Bts, ip = bts)
        freqs = [str(x) for x in bts.freCs.split('/')]
        for frec in freqs:
            frequencies.append(frec)

    assigned = [ str(x) for x in nvf.bts.freCs.split('/') ]

    while (True):
        if not str(start)+'-'+str(int(start)+int(nvf.BW_UL)) in frequencies:
            if not str(start)+'-'+str(int(start)+int(nvf.BW_UL)) in assigned:
                nvf.bts.freCs = str(nvf.bts.freCs)+'/'+str(start)+'-'+str(int(start)+int(nvf.BW_UL))
                nvf.freC_UL = int(start)+int(nvf.BW_UL)/2
                break
            else:
                start = int(start)+int(nvf.BW_UL)
        else:
            start = int(start)+int(nvf.BW_UL) 
    nvf.save()
    bts.save()
    return nvf.bts.freCs

