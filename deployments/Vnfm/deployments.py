from jinja2 import Template
from VIM.OpenStack.keystone.keystone import auth
from VIM.OpenStack.heat.heat import create_stack, delete_stack


def create(user, name, description, lista):
    nvf_list = []

    header = Template(u'''\
heat_template_version: 2015-10-15
description: {{description}}

parameters:
  NetID:
    type: string
    description: Network ID to use for the instance.
    default: 0e67e979-6fb8-485a-923f-1c5d57351e76
resources:
  ''')
    header = header.render(
        description=description,
    )

    nvfi = ""
    num = 0
    for bts in lista:
        nvf = Template(u'''\
server{{num}}:
    type: OS::Nova::Server
    properties:
      image: {{image}}
      flavor: {{flavor}}
      networks:
      - network: { get_param: NetID }

  ''')

        nvf = nvf.render(
            name=bts.bts.name,
            image="UBU1404SERVER6GUHD380srsLTE_AUTOSTART",
            # flavor = bts.split(',')[4],
            flavor="m1.small",
            freC=bts.freC_DL,
            ip=bts.name.split('-')[1],
            num=num,
        )
        nvfi = nvfi + nvf
        nvf_list.append(bts)
        num=num+1

    outfile = open('/home/howls/Apps/OOCRAN/aloeo/resources/deployments/yaml/' + name + '.yaml', 'w')
    outfile.write(header + nvfi)
    outfile.close()

    create_stack(name,'/home/howls/Apps/OOCRAN/aloeo/resources/deployments/yaml/' + name + '.yaml', auth(user), user.id_project)


def delete(token, name):
    delete_stack(name)
