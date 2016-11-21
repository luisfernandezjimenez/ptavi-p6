#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Programa cliente que abre un socket a un servidor."""

import socket
import sys

# Cliente UDP simple.
try:

    METODO = sys.argv[1]
    RECEPTOR = sys.argv[2].split('@')[0]
    IP = sys.argv[2].split('@')[1].split(':')[0]
    PUERTO = sys.argv[2].split('@')[1].split(':')[1]
except IndexError:
    print('Usage: python client.py method receiver@IP:SIPport')

# Contenido que vamos a enviar --> Peticion SIP
LINEA = METODO.upper() + ' sip:' + RECEPTOR + '@' + IP + ' SIP/2.0\r\n\r\n'

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((IP, int(PUERTO)))

print("Enviando: " + LINEA)
my_socket.send(bytes(LINEA, 'utf-8') + b'\r\n')
data = my_socket.recv(1024)
print('Recibido -- ', data.decode('utf-8'))

respuesta = data.decode('utf-8').split('\r\n')[0:-2]
if respuesta == ['SIP/2.0 100 Trying', '', 'SIP/2.0 180 Ringing', '',
                 'SIP/2.0 200 OK']:
    METODO = 'ACK'
    LINEA_ACK = METODO + ' sip:' + RECEPTOR + '@' + IP + ' SIP/2.0\r\n\r\n'
    print("Enviando: " + LINEA_ACK)
    my_socket.send(bytes(LINEA_ACK, 'utf-8'))
    data = my_socket.recv(1024)

print("Terminando socket...")


# Cerramos todo
my_socket.close()
print("Fin.")
