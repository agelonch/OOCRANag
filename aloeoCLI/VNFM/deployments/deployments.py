from jinja2 import Template

from VIM.OpenStack import heat


def create(token, username, name, description, lista):
    nvf_list = []

    header = Template(u'''\
heat_template_version: 2013-05-23

description: {{description}}

parameters:
  image:
    type: string
    description: Name of image to use for servers
    default: UBU1404SERVER6GUHD380srsLTE_AUTOSTART
  flavor:
    type: string
    description: Flavor to use for servers
    default: m1.small

resources:
  
  ''')
    header = header.render(
        description=description,
    )

    nvfi = ""
    for bts in lista:
        nvf = Template(u'''\
{{ip}}:
    type: OS::Nova::Server
    properties:
      name: {{ip}}
      image: {{image}}
      flavor: {{flavor}}
      networks:
        - network: selfservice
      user_data_format: RAW
      user_data: |
        #cloud-config
        chpasswd:
          list: |
            ubuntu:ubuntu
          expire: False
        hostname: {{ip}}
        fqdn: {{ip}}
        manage_etc_hosts: true
        write_files:
          - path: /home/nodea/autorun.sh
            permissions: "0777"
            content: |
                 cd /home/nodea/DADES_TX/srsLTE/build/srslte/examples
                 ./pdsch_enodeb_multiUser -l 0.3 -g 40.0 -p 6 -i rfc793.txt -o prova.txt
        runcmd:
         - sudo chmod 777 /home/nodea/autorun.sh
  ''')

        nvf = nvf.render(
            name=bts.bts.name,
            image="TX_LTE",
            # flavor = bts.split(',')[4],
            flavor="m1.small",
            freC=bts.freC_DL,
            ip=bts.name,
        )
        nvfi = nvfi + nvf
        nvf_list.append(bts)

    outfile = open('/home/howls/Apps/OOCRAN/aloeo/resources/deployments/yaml/' + name + '.yaml', 'w')
    outfile.write(header + nvfi)
    outfile.close()

    heat.Heat(token, username).create_stack(name, '/home/howls/Apps/OOCRAN/aloeo/resources/deployments/yaml/' + name + '.yaml')


def delete(token, username, name):
    heat.Heat(token, username).delete_stack(name)
