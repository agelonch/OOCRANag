from credentials import get_nova_credentials_v2
from novaclient.client import Client
from novaclient.v2.flavors import Flavor


def create_flavor(name, cpu, ram):
    nova_client = Client(version='2',
                         username='admin',
                         api_key='odissey09',
                         auth_url='http://147.83.118.228:5000/v2.0/',
                         project_id='admin')

    nova_client.flavors.create(name=name, ram=ram, vcpus=1, disk=20, flavorid='auto', ephemeral=0, swap=0,
                               rxtx_factor=1.0, is_public=True)

    period = 5000 / (100 / int(cpu))

    flavor = nova_client.flavors.find(name=name)
    flavor.set_keys({"quota": "cpu_quota=5000", "period": "cpu_period=" + str(period)})


def flavor(name, values):
    lista = []

    create_flavor(name, values[0][0], values[0][0])
    lista.append(name)

    return lista


def find_vm(name):
    print "prova"
    '''nova_client = Client(version='2',
                         username='operator1',
                         api_key='odissey09',
                         auth_url='http://147.83.118.228:5000/v2.0/',
                         project_id='operator1')'''
    credentials = get_nova_credentials_v2()
    nova_client = Client(**credentials)
    print "dins"
    print(nova_client.servers.list())
    print "fora"
    #return nova_client.servers.find(name=name)
