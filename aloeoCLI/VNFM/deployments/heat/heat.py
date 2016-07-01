import os
import sys
from time import sleep
#import aloeoCLI.tasks.configuration as conf
from keystoneclient.auth.identity import v2 as identity
from keystoneclient import session
from heatclient.client import Client
from keystone import keystone
#import aloeoCLI.tasks.configuration as conf

class Heat:

   def __init__(self, token, name):
      tenant = keystone.get_tenant(name)
      self.heat = Client('1', endpoint="http://controller:8004/v1/"+str(tenant), token=token)

   def create_stack(self, name, file):
      
      template_file = file 
      template = open(template_file, 'r')
      stack = self.heat.stacks.create(stack_name=name, template=template.read(), parameters={})
      uid = stack['stack']['id']

      stack = self.heat.stacks.get(stack_id=uid).to_dict()
      while stack['stack_status'] == 'CREATE_IN_PROGRESS':
         print "INFO: Creating stack."
         stack = self.heat.stacks.get(stack_id=uid).to_dict()
         sleep(10)
      
      if stack['stack_status'] == 'CREATE_COMPLETE':
         print "INFO: Stack succesfully created."
      else:
         raise Exception("INFO: Stack fall to unknow status: {}".format(stack))

   def delete_stack(self, name):
      stack = self.heat.stacks.get(name)      
      self.heat.stacks.delete(stack.parameters['OS::stack_id'])
      print "INFO: Default stack deleted."

   def list(self):   
      stacks = self.heat.stacks.list()
      while True:
       try:
           stack = stacks.next()
           print stack.stack_name+" ("+stack.id+"): "+stack.stack_status
       except StopIteration:
           break
