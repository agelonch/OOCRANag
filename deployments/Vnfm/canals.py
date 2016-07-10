from jinja2 import Template
from VIM.OpenStack.keystone.keystone import auth
from VIM.OpenStack.heat.heat import create_stack, delete_stack


def create_channel(user, name, description, instance):
    nvf_list = []

    header = Template(u'''\
heat_template_version: 2015-10-15
description: {{description}}

parameters:
  NetID:
    type: string
    description: Network ID to use for the instance.
    default: 6de45ecf-4aac-4161-bd8c-ce24951ef6d2
resources:
  ''')
    header = header.render(
        description=description,
    )

    nvfi = ""
    nvf = Template(u'''\
channel{{num}}:
    type: OS::Nova::Server
    properties:
      image: {{image}}
      flavor: {{flavor}}
      networks:
      - network: {{net}}_canal_net
      user_data_format: RAW
      user_data: |
        #cloud-config
        runcmd:
         - echo "{{script}}" >> /home/nodea/start.sh
         - sh /home/nodea/start.sh

  ''')

    nvf = nvf.render(
        name=instance.name,
        image=instance.image,
        # flavor = bts.split(',')[4],
        net=instance.area.name,
        flavor="m1.small",
        #script=str(bts.vnf.script).replace('\n', '').replace('\r', ';').replace('{{ip}}',bts.name.split('-')[1]).replace('{{pt}}',str(bts.Pt)).replace('{{freC}}',str(frec)).replace('{{BW}}',str(f)),
    )
    nvfi = nvfi + nvf

    outfile = open('/home/howls/Apps/OOCRAN/aloeo/resources/deployments/yaml/' + name + '.yaml', 'w')
    outfile.write(header + nvfi)
    outfile.close()

    create_stack(name, '/home/howls/Apps/OOCRAN/aloeo/resources/deployments/yaml/' + name + '.yaml', auth(user),
                 user.id_project)


def delete_channel(name, user):
    delete_stack(name, auth(user),user.id_project)