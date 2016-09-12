from jinja2 import Template
from VIM.OpenStack.keystone.keystone import auth
from VIM.OpenStack.heat.heat import create_stack, delete_stack


def infrastructure(user, name, description):
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

  {{name}}_canal_router:
    type: OS::Neutron::Router
    properties:
      name: {{name}}_canal_router
      external_gateway_info:
        network: 0e67e979-6fb8-485a-923f-1c5d57351e76

  {{name}}_canal_usrp_interface:
    type: OS::Neutron::RouterInterface
    properties:
      router_id: { get_resource: {{name}}_canal_router }
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

  {{name}}_bts_router:
    type: OS::Neutron::Router
    properties:
      name: {{name}}_bts_router
      external_gateway_info:
        network: 0e67e979-6fb8-485a-923f-1c5d57351e76

  {{name}}_canal_bts_interface:
    type: OS::Neutron::RouterInterface
    properties:
      router_id: { get_resource: {{name}}_bts_router }
      subnet_id: { get_resource: {{name}}_bts_subnet }

  {{name}}_subs_net:
    type: OS::Neutron::Net
    properties:
      name: {{name}}_subs_net

  {{name}}_subs_subnet:
    type: OS::Neutron::Subnet
    properties:
      name: {{name}}_subs_subnet
      network_id: { get_resource: {{name}}_subs_net }
      cidr: 30.0.0.0/24
      gateway_ip: 30.0.0.1
      allocation_pools:
        - start: 30.0.0.2
          end: 30.0.0.254

  {{name}}_subs_router:
    type: OS::Neutron::Router
    properties:
      name: {{name}}_subs_router
      external_gateway_info:
        network: 0e67e979-6fb8-485a-923f-1c5d57351e76

  {{name}}_subs_interface:
    type: OS::Neutron::RouterInterface
    properties:
      router_id: { get_resource: {{name}}_subs_router }
      subnet_id: { get_resource: {{name}}_subs_subnet }

     
  ''')
    header = header.render(
        description=description,
        name=name
    )

    outfile = open('/home/antoni/DADES/OOCRAN/OOCRAN/OOCRAN/aloeo/resources/scenarios/yaml/' + name + '.yaml', 'w')
    outfile.write(header)
    outfile.close()

    create_stack(name,'/home/antoni/DADES/OOCRAN/OOCRAN/OOCRAN/aloeo/resources/scenarios/yaml/' + name + '.yaml', auth(user), user.id_project)
