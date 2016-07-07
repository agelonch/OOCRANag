#import pysftp

def get_logs():
	with pysftp.Connection('controller', username='odissey09', password='odissey@09') as sftp:
		with sftp.cd('aloeo'):
			sftp.get_d('logs','/home/howls/Documents/tfm/aloeo/logs')

def send_service(user, password, ip):
	with pysftp.Connection(ip, username=user, password=password) as sftp:
		with sftp.cd('aloeo/demo/benchmark'):
			sftp.put('/home/howls/tfm/aloeo/resources/vnfs/modules/vnf.zip')

'''sudo iptables -t nat -A PREROUTING -p tcp --dport 110 -j DNAT --to-destination 192.168.10.10:22
sudo iptables -t nat -A PREROUTING -p tcp --dport 111 -j DNAT --to-destination 192.168.10.11:22
sudo iptables -t nat -A PREROUTING -p tcp --dport 112 -j DNAT --to-destination 192.168.10.12:22
sudo iptables -t nat -A PREROUTING -p tcp --dport 113 -j DNAT --to-destination 192.168.10.13:22
sudo iptables -t nat -A PREROUTING -p tcp --dport 114 -j DNAT --to-destination 192.168.10.14:22
sudo iptables -t nat -A PREROUTING -p tcp --dport 115 -j DNAT --to-destination 192.168.10.15:22
sudo iptables -t nat -A PREROUTING -p tcp --dport 116 -j DNAT --to-destination 192.168.10.16:22
sudo iptables -t nat -A PREROUTING -p tcp --dport 117 -j DNAT --to-destination 192.168.10.17:22
sudo iptables -t nat -A PREROUTING -p tcp --dport 118 -j DNAT --to-destination 192.168.10.18:22
sudo iptables -t nat -A PREROUTING -p tcp --dport 119 -j DNAT --to-destination 192.168.10.19:22
sudo iptables -t nat -A PREROUTING -p tcp --dport 120 -j DNAT --to-destination 192.168.10.20:22
sudo iptables -t nat -A PREROUTING -p tcp --dport 121 -j DNAT --to-destination 192.168.10.21:22
sudo iptables -t nat -A PREROUTING -p tcp --dport 122 -j DNAT --to-destination 192.168.10.22:22
sudo iptables -t nat -A PREROUTING -p tcp --dport 123 -j DNAT --to-destination 192.168.10.23:22
sudo iptables -t nat -A PREROUTING -p tcp --dport 124 -j DNAT --to-destination 192.168.10.24:22
sudo iptables -t nat -A PREROUTING -p tcp --dport 125 -j DNAT --to-destination 192.168.10.25:22
sudo iptables -t nat -A PREROUTING -p tcp --dport 126 -j DNAT --to-destination 192.168.10.26:22
sudo iptables -t nat -A PREROUTING -p tcp --dport 127 -j DNAT --to-destination 192.168.10.27:22
sudo iptables -t nat -A PREROUTING -p tcp --dport 128 -j DNAT --to-destination 192.168.10.28:22
sudo iptables -t nat -A PREROUTING -p tcp --dport 129 -j DNAT --to-destination 192.168.10.29:22
sudo iptables -t nat -A PREROUTING -p tcp --dport 130 -j DNAT --to-destination 192.168.10.30:22'''
