#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# Programa Cliente
# www.pythondiario.com
import socket
import sys
import json

def send(bts):
    # Creando un socket TCP/IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     
    # Conecta el socket en el puerto cuando el servidor esté escuchando
    server_address = ('localhost', 10003)
    print >>sys.stderr, 'conectando a %s puerto %s' % server_address
    sock.connect(server_address)

    message = []

    for key,value in bts.items():
        msn = {"BTS":key,"data":'./pdsch_enodeb_file -i ../../../rfc793.txt -n 100000 -I 127.0.0.1 -P 8888'}
        message.append(msn)

    try: 
        # Enviando datos
        message = json.dumps(message, separators=(',',':'))

        sock.sendall(message)
     
        # Buscando respuesta
        amount_received = 0
        amount_expected = len(message)
         
        #while amount_received < amount_expected:
        data = sock.recv(19)
        amount_received += len(data)
        print >>sys.stderr, 'recibiendo "%s"' % data
               
    finally:
        sock.close()
