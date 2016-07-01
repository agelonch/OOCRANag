import os
from keystoneclient.v2_0 import client

def get_tenant(name):
   keystone = client.Client(username="admin", 
                            password="odissey09" ,
                            tenant_name="admin", 
                            auth_url="http://controller:5000/v2.0/")

   tenants = keystone.tenants.list()
   my_tenant = [x for x in tenants if x.name==name][0]

   return my_tenant.id
