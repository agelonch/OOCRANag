import os
import yaml
import shutil
import aloeoCLI.VNFM.configuration as conf
from jinja2 import Template


def main(name, description, flavors=None):   

  if flavors == None:
     flavors = "m1.small"

  nvfi=''
  parameters=''

  #Header#
  header = Template(u'''\
heat_template_version: 2013-05-23

description: HOT template to deploy two servers to an existing Neutron network.

parameters:
  image:
    type: string
    description: Name of image to use for servers
    default: ALOE_V0.0
  flavor:
    type: string
    description: Flavor to use for servers
    default: m1.small

resources:
  server:
    type: OS::Nova::Server
    properties:
      name: {{name}}
      image: {{image}}
      flavor: {{flavor}}
      networks:
        - network: private
      user_data_format: RAW
      user_data: |
        #cloud-config
        chpasswd:
          list: |
            ubuntu:ubuntu
          expire: False
        hostname: {{name}}
        fqdn: {{name}}
        manage_etc_hosts: true
        write_files:
          - path: /home/nodea/service.sh
            permissions: "0777"
            content: |
                 cd /home/nodea/DADES/ALOE-1.6_WORKING_DEC15V1/scripts/
                 ./create_module_templateSK15.sh chaintest
                 cd ..
                 ./scripts/update_modules.pl
                 cd modules/chaintest/src

                 lftp -p 22 -u odissey09,odissey@09 sftp://192.168.10.100 << CMD
                 cd aloeo/demo/benchmark
                 get vnf.zip
                 bye
                 CMD

                 unzip vnf.zip
                 rm vnf.zip

                 cd chaintest
                 mv * ../
                 cd ..
                 rm -r chaintest/

                 cd /home/nodea/DADES/ALOE-1.6_WORKING_DEC15V1/
                 ./configureALL.sh
                 sudo make install
                 cd /home/nodea
                 sh autostart.sh
        runcmd:
         - sudo chmod 777 /home/nodea/service.sh
  ''')

  header = header.render(
      name = name,
      image = "VM-0.1.1",
      flavor = flavors,
      path = "/home/nodea/DADES/ALOE-1.6_WORKING_DEC15V1/",
      user = "operator1",
      password = "odissey09",
      IP = "192.168.10.100",
  )

  outfile = open('/home/howls/tfm/aloeo/resources/vnfs/yaml/'+name+'.yaml', 'w') 
  outfile.write(header)
  outfile.close()