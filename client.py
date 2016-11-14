#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket

# Cliente UDP simple.
try:
    METODO = sys.argv[1]
    RECEPTOR = sys.argv[2] + '@'
    #RECEPTOR = sys.argv[2] + '@' + sys.argv[3] + ':' + int(sys.argv[5])#2
    IP = sys.argv[3] + ':'
    PORT = int(sys.argv[4])
    #EXPIRES = int(sys.argv[5])
except IndexError:
    print('Usage: python client.py method receiver@IP:SIPport')

# Dirección IP del servidor.
SERVER = 'localhost'
PORT = 6001

# Contenido que vamos a enviar
LINE = (METODO.upper() + RECEPTOR + IP + PORT)
#LINE = (METODO.upper() + RECEPTOR)#2


#LINE = '¡Hola mundo!'

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

print("Enviando: " + LINE)
my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
data = my_socket.recv(1024)

print('Recibido -- ', data.decode('utf-8'))
print("Terminando socket...")

# Cerramos todo
my_socket.close()
print("Fin.")

#COMUNICACION SIP SENCILLA QUE EL CLIENTE MANDA UN BYTE AL SERVIDOR Y ESTE ULTIMO
#LO TRATARA
#METODO = INVITE o ACK o BYE
#iINVITE --> SIN PUERTO
#ACK --> NOS RESPONDE EL OTRO LADO DICIENDO ESTOY LISTO
#BYE --> FINALIZO CONVER

#SERVIDORA:
#RESPONDE --> 100 180 200 400 405
#LOS 3 PRIMEROS EN UN SOLO MENSAJE
