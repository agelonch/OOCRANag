#!/usr/bin/env python

from ConfigParser import ConfigParser

def read():
	config=ConfigParser()
	config.read("/home/howls/Documents/tfm/aloeo/Orchestrator/aloeoCLI/aloeo.conf")
	return config
def get_aloeo_path():
	config = read()	
	path = config.get("ALOEO", "aloeo_path")
	return path

def get_template_path():
	config = read()	
	path = config.get("ALOEO", "template_path")
	return path

def get_endpoint_heat():
	config = read()	
	path = config.get("ALOEO", "endpoint_heat")
	return path

def get_endpoint_nova():
	config = read()	
	path = config.get("ALOEO", "endpoint_nova")
	return path

def get_endpoint_keystone():
	config = read()	
	path = config.get("ALOEO", "endpoint_keystone")
	return path

def get_endpoint_ceilometer():
	config = read()	
	path = config.get("ALOEO", "endpoint_ceilometer")
	return path

def get_vnf_path():
	config = read()
	path = config.get("VNF", "aloe_path")
	return path

def get_vnf_image():
	config = read()
	path = config.get("VNF", "VNF_image")
	return path

def get_server_ip():
	config = read()
	path = config.get("ALOEO", "server_ip")
	return path





