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
    default: 6de45ecf-4aac-4161-bd8c-ce24951ef6d2
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
      user_data_format: RAW
      user_data: |
        #cloud-config
        runcmd:
         - echo "cd /home/nodea/DADES/TX_LTE/srsLTE/build/srslte/examples" >> /home/nodea/start.sh
         - echo "./pdsch_enodeb_file -a addr={{ip}} -l 0.3 -g {{pt}} -f {{freC}} -p {{BW}} -i ../../../rfc793.txt -m 1 >> /home/nodea/run.log" >> /home/nodea/start.sh
         - sh /home/nodea/start.sh

  ''')
        if bts.BW_DL == 1400000:
            f = 6
        if bts.BW_DL == 3000000:
            f = 3

        frec =2393000000
        if bts.name.split('-')[1] == "192.168.10.2":
            frec= 2392100000

        nvf = nvf.render(
            name=bts.bts.name,
            image="UBU1404SERVER6GUHD380srsLTE_AUTOSTART",
            # flavor = bts.split(',')[4],
            flavor="m1.small",
            freC=frec,
            ip=bts.name.split('-')[1],
            num=num,
            pt=bts.Pt,
            BW=f,
        )
        nvfi = nvfi + nvf
        nvf_list.append(bts)
        num = num + 1

    outfile = open('/home/howls/Apps/OOCRAN/aloeo/resources/deployments/yaml/' + name + '.yaml', 'w')
    outfile.write(header + nvfi)
    outfile.close()

    create_stack(name, '/home/howls/Apps/OOCRAN/aloeo/resources/deployments/yaml/' + name + '.yaml', auth(user),
                 user.id_project)


def delete(name, user):
    delete_stack(name, auth(user),user.id_project)
