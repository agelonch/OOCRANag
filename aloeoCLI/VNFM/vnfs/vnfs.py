import os
import aloeoCLI.tasks.configuration as conf
import yaml
from jinja2 import Template

from aloeoCLI.VNFM.vnfs.modules import parser_creation
import aloeoCLI.VNFM.vnfs.modules.ftp as ftp

from aloeoCLI.VIM.OpenStack.heat import heat
from aloeoCLI.VIM.OpenStack.nova import nova
from aloeoCLI.VIM.OpenStack.ceilometer import ceilometer
from aloeoCLI.VIM.OpenStack.heat import heat


def create(token, username, name, description):
   Heat = heat.Heat(token,username)
   ftp.send_service("odissey09","odissey@09", "controller")

   name = parser_creation.parser_create_template(name, description)
   Heat.create_stack(name,'/home/howls/tfm/aloeo/resources/vnfs/yaml/'+name+'.yaml')
   results = ceilometer.monitor_resources(name)
   nova.flavor(name, results)
   parser_creation.parser_create_template(name, description, name)
   Heat.delete_stack(name)

   return results

