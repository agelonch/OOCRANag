import os
import yaml
import shutil
from jinja2 import Template

def main(name, description, inputs, con_in, con_out, functions, flavors=None):   

  if flavors == None:
     flavors = []
     for i in range(len(functions)):
        flavors.append('m1.small')

  nvfi=''
  nfv=0

  header = Template(u'''\
heat_template_version: 2013-05-23

description: HOT template to deploy two servers to an existing Neutron network.

parameters:
  image:
    type: string
    description: Name of image to use for servers
    default: ubuntu
  flavor:
    type: string
    description: Flavor to use for servers
    default: flavor
  net_id:
    type: string
    description: ID of Neutron network into which servers get deployed
    default: 473b9606-f7b9-4286-8d3f-1cd3112e281d
  subnet_id:
    type: string
    description: ID of Neutron sub network into which servers get deployed
    default: 5ae7eec3-01d6-4e37-ad8b-d840701e5d17

resources:
  ''')

  header = header.render(
      name = name,
      description = description
  )

  for func in functions:

    body = Template(u'''\

  server{{nfv}}:
    type: OS::Nova::Server
    properties:
      name: {{name}}
      image: { get_param: image }
      flavor: {{flavor}}
      networks:
        - port: { get_resource: server{{nfv}}_port }
      user_data_format: RAW
      user_data: |
        #cloud-config
        final_message: "Templated created"
        runcmd:
         - sed -i 's/##code##/{{function}}/' aloefile.conf
         - runcf
     
  server{{nfv}}_port:
    type: OS::Neutron::Port
    properties:
      network_id: { get_param: net_id }
      fixed_ips:
        - subnet_id: { get_param: subnet_id }
    ''')
  
    func = body.render(
          nfv = nfv,
          name = func,
          id = name,
          function=functions[func],
          flavor=flavors[nfv]
    )
    nvfi = nvfi + func
    nfv=nfv+1

  outfile = open('/home/howls/Documents/tfm/aloeo/templates/'+name+'.yaml', 'w') 
  outfile.write(header+nvfi)
  outfile.close()

