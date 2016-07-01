#!/usr/bin/python
import sqlite3
import time
import heat.heat as heat
from keystoneclient.auth.identity import v2 as identity
from keystoneclient import session
import sys
from datetime import datetime

def auth():
  try:
  	auth = identity.Password(auth_url="http://controller:5000/v2.0/",
                             username="operator1",
                           	 password="odissey09",
                             tenant_name="operator1")

  	sess = session.Session(auth=auth)
  	token = auth.get_token(sess)
  	print "INFO: Authentification succesfully."
  except:
    print "INFO: Authentification failed."
    sys.exit(130)

  return token

def opt(id):
	print "dins"
	conn = sqlite3.connect('/home/howls/tfm/aloeo/NFVO/db.sqlite3')
	c.execute("SELECT * FROM vnfs_operator WHERE ID = "+str(id))
	rows1 = c.fetchall()
	for row in rows1:
		print row[3]
		return row[3]


conn = sqlite3.connect('/home/howls/tfm/aloeo/NFVO/db.sqlite3')
c = conn.cursor()
c.execute("SELECT * FROM scenarios_area")
rows = c.fetchall()

print time.strftime("%H:%M:%S")

for row in rows:
	forecast = row[9][1:][:-1].split(',')
	print "previsio"
	print forecast[int(time.strftime("%H"))]
	print "oferta actual"
	oferta = row[10][1:][:-1].split(',')
	print oferta[int(time.strftime("%H"))]
	#heat.Heat(auth(), opt(id=operator)).create_stack(name, '/home/howls/tfm/aloeo/resources/deployments/yaml/'+name+'.yaml')
	#time.sleep(10)
	print "#############################################################################"
	

archi=open('/home/howls/tfm/aloeo/NFVO/aloeoCLI/VNFM/deployments/datos.txt','w')
archi.close()

print "read succesfull"

