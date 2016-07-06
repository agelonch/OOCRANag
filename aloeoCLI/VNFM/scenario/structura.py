from jinja2 import Template

from VIM.OpenStack import heat


def infrastructure(token, username, name ,description):
  
  header = Template(u'''\
heat_template_version: 2013-05-23

description: {{description}}

parameters:
  image:
    type: string
    description: Name of image to use for servers
    default: LTE
  flavor:
    type: string
    description: Flavor to use for servers
    default: m1.small

resources:
  {{name}}_canal_net:
    type: OS::Neutron::Net
    properties:
      name: {{name}}_canal_net

  {{name}}_canal_subnet:
    type: OS::Neutron::Subnet
    properties:
      network_id: { get_resource: {{name}}_canal_net }
      cidr: 10.0.0.0/24
      gateway_ip: 10.0.0.1
      allocation_pools:
        - start: 10.0.0.3
          end: 10.0.0.254

  {{name}}_router:
    type: OS::Neutron::Router
    properties:
      name: {{name}}_router
      external_gateway_info:
        network: 887bf999-8643-4271-9fcf-3a508b4c246e

  {{name}}_canal_usrp_interface:
    type: OS::Neutron::RouterInterface
    properties:
      router_id: { get_resource: {{name}}_router }
      subnet_id: { get_resource: {{name}}_canal_subnet }

  {{name}}_bts_net:
    type: OS::Neutron::Net
    properties:
      name: {{name}}_bts_net

  {{name}}_bts_subnet:
    type: OS::Neutron::Subnet
    properties:
      network_id: { get_resource: {{name}}_bts_net }
      cidr: 20.0.0.0/24
      gateway_ip: 20.0.0.1
      allocation_pools:
        - start: 20.0.0.2
          end: 20.0.0.254

  {{name}}_canal_bts_interface:
    type: OS::Neutron::RouterInterface
    properties:
      router_id: { get_resource: {{name}}_router }
      subnet_id: { get_resource: {{name}}_bts_subnet }
     
  ''')
  header = header.render(
      description = description,
      name = name
  	)
      
  outfile = open('/home/howls/Apps/OOCRAN/aloeo/resources/scenarios/yaml/'+name+'.yaml', 'w')
  outfile.write(header)
  outfile.close()

  heat.Heat(token, username).create_stack(name, '/home/howls/Apps/OOCRAN/aloeo/resources/scenarios/yaml/' + name + '.yaml')