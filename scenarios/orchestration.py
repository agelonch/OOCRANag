import numpy as np

def scenarioCreate(file):
	btss = np.genfromtxt(file,dtype='str')
	lista_bts= []

	for bts in btss:
	    vm = {}
	    vm['name'] = bts.split(',')[0]
	    vm['ip'] = bts.split(',')[1]
	    vm['lat'] = bts.split(',')[2]
	    vm['long'] = bts.split(',')[3]
	    vm['r_max'] = bts.split(',')[4]
	    vm['neighbor'] = bts.split(',')[5]
	    vm['bw'] = bts.split(',')[6]
	    lista_bts.append(vm)

	return lista_bts