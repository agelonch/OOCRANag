#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# Programa Servidor
# www.pythondiario.com
import socket
import sys
import json
import ast


def send(tx,data):
    # Creando un socket TCP/IP
    sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    message = data
    print data
    # Conecta el socket en el puerto cuando el servidor esté escuchando
    server_address = (tx, 10003)
    print >>sys.stderr, 'conectando a %s puerto %s' % server_address
    sock1.connect(server_address)

    try: 
        # Enviando datos
        sock1.sendall(message)
     
        # Buscando respuesta
        amount_received = 0
        amount_expected = len(message)
         
        #while amount_received < amount_expected:
        data = sock1.recv(19)
        amount_received += len(data)
        print >>sys.stderr, 'recibiendo "%s"' % data
               
    finally:
        sock1.close()



# Creando el socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Enlace de socket y puerto
server_address = ('localhost', 10003)
print >>sys.stderr, 'empezando a levantar %s puerto %s' % server_address
sock.bind(server_address)
# Escuchando conexiones entrantes
sock.listen(1)

while True:
    # Esperando conexion
    print >>sys.stderr, 'Esperando para conectarse'
    connection, client_address = sock.accept()
 
    try:
        # Recibe los datos en trozos y reetransmite
        while True:
            data = connection.recv(1024)
            data = json.loads(data)
            for bts in data:
                send(bts['BTS'],bts['data'])

            if data:
                connection.sendall("OK")
            else:
                break
             
    finally:
        # Cerrando conexion
        print "connecion finished"
        connection.close()
