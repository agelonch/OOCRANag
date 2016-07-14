from jinja2 import Template
from VIM.OpenStack.keystone.keystone import auth
from VIM.OpenStack.heat.heat import create_stack, delete_stack


def create(user, name, description, bts, channels):

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
    num = 0
    for bt in bts:
        nvf = Template(u'''\
server{{num}}:
    type: OS::Nova::Server
    properties:
      name: {{name}}
      image: {{image}}
      flavor: {{flavor}}
      networks:
      - network: {{net}}_bts_net
      user_data_format: RAW
      user_data: |
        #cloud-config
        runcmd:
         - echo "{{script}}" >> /home/nodea/start.sh
         - sh /home/nodea/start.sh

  ''')

        if bt.BW_DL == 1400000:
            f = 6
        if bt.BW_DL == 3000000:
            f = 3

        frec =2393000000
        if bt.name.split('-')[1] == "192.168.10.2":
            frec= 2392100000

        nvf = nvf.render(
            name=bt.bts.name,
            image=bt.vnf.image,
            # flavor = bts.split(',')[4],
            net=bt.bts.area.name,
            flavor="m1.small",
            num=num,
            script=str(bt.vnf.script).replace('\n', '').replace('\r', ';').replace('{{ip}}',bt.name.split('-')[1]).replace('{{pt}}',str(bt.Pt)).replace('{{freC}}',str(frec)).replace('{{BW}}',str(f)),
        )
        nvfi = nvfi + nvf
        num = num + 1

    num = 0
    for channel in channels:
        canal = Template(u'''\
channel{{num}}:
    type: OS::Nova::Server
    properties:
      name: {{name}}
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

        canal = canal.render(
            name=channel.name,
            image=channel.vnf.image,
            # flavor = bts.split(',')[4],
            net=channel.deploy.area.name,
            flavor="m1.small",
            num=num,
            script=str(channel.vnf.script).replace('\n', '').replace('\r', ';').replace('{{ip}}',channel.ip).replace('{{snr}}',channel.snr),
        )
        nvfi = nvfi + canal
        num = num + 1

    outfile = open('/home/howls/Apps/OOCRAN/aloeo/resources/deployments/yaml/' + name + '.yaml', 'w')
    outfile.write(header + nvfi)
    outfile.close()

    create_stack(name, '/home/howls/Apps/OOCRAN/aloeo/resources/deployments/yaml/' + name + '.yaml', auth(user),
                 user.id_project)


def delete(name, user):
    delete_stack(name, auth(user),user.id_project)
