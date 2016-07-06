import ceilometerclient.v2 as c_client
import keystoneclient.v2_0.client as k_client
import time

from VIM import nova


def statistics(vm, name):
   
   keystone = k_client.Client(auth_url='http://controller:5000/v2.0/', 
                              username='admin',
                              password='odissey09', 
                              tenant_name='admin')

   auth_token = keystone.auth_token
   ceilometer = c_client.Client(endpoint='http://controller:8777', token= lambda : auth_token )

   query = [dict(field='resource_id', op='eq', value=vm), 
            dict(field='meter',op='eq',value='cpu_util')]
   cpu = ceilometer.statistics.list('cpu_util',q=query)
   cpu_p = cpu[0]
   cpu = cpu_p.avg
   cpu = round(float(cpu))+1
   cpu_GHz = (2.3*1000)*(cpu/100)

   query = [dict(field='resource_id', op='eq', value=vm)]
   ram = ceilometer.statistics.list('memory.usage', q=query)
   ram_p = ram[0]
   ram = ram_p.avg
   ram = int(round(float(ram))+1)+1000

   '''query = [dict(field='resource_id', op='eq', value='instance-0000035f-'+vm+'-tapd93451e3-41')]
   net = ceilometer.statistics.list('network.outgoing.bytes.rate')
   print net

   query = [dict(field='resource_id', op='eq', value='instance-0000035f-'+vm+'-tapd93451e3-41')]
   net = ceilometer.statistics.list('network.incoming.bytes.rate')
   print net'''

   print "INFO: For "+name+" the cpu_usage: "+str(cpu_GHz)+" MHz ("+str(int(cpu))+" %) and RAM memory: "+str(ram)+" MB."
   return str(int(cpu)), ram

def monitor_resources(name):
   print 'INFO: Monitoring resources.'
   time.sleep(63) #180
   results = []
   id = nova.find_vm(name)
   results.append(statistics(id.id, name)) 

   return results

