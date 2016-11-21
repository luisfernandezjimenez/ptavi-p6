#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Clase (y programa principal) para un servidor de eco en UDP simple."""

import socketserver
import sys
import os


class EchoHandler(socketserver.DatagramRequestHandler):
    """Echo server class."""

    def handle(self):
        u"""Implementación de los Metodos INVITE, ACK y BYE."""
        # Escribe dirección y puerto del cliente (de tupla client_address)
        print("La direccion y puerto del cliente es: " +
              str(self.client_address))
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            linea_cliente = self.rfile.read()
            metodo_cliente = linea_cliente.decode('utf-8').split(' ')[0]
            # Si no hay más líneas salimos del bucle infinito
            if not linea_cliente:
                break

            print("El cliente nos manda " + linea_cliente.decode('utf-8'))

            if metodo_cliente not in metodosposibles:
                respuesta = ("SIP/2.0 405 Method Not Allowed" + '\r\n\r\n')
                self.wfile.write(bytes(respuesta, 'utf-8'))

            elif metodo_cliente == 'INVITE':
                respuesta = ("SIP/2.0 100 Trying" + '\r\n\r\n' +
                             "SIP/2.0 180 Ringing" + '\r\n\r\n' +
                             "SIP/2.0 200 OK" + '\r\n\r\n')
                self.wfile.write(bytes(respuesta, 'utf-8'))

            elif metodo_cliente == 'ACK':
                aEjecutar = ('mp32rtp -i ' + self.client_address[0] +
                             ' -p 23032 < ' + FICHERO_AUDIO)
                print("Vamos a ejecutar", aEjecutar)
                os.system(aEjecutar)

            elif metodo_cliente == 'BYE':
                respuesta = ("SIP/2.0 200 OK" + '\r\n\r\n')
                self.wfile.write(bytes(respuesta, 'utf-8'))
                print('Finish...')

            else:
                respuesta = ("SIP/2.0 400 Bad Request" + '\r\n\r\n')
                self.wfile.write(bytes(respuesta, 'utf-8'))

if __name__ == "__main__":
    try:
        SERVIDOR = sys.argv[1]
        PUERTO = sys.argv[2]
        FICHERO_AUDIO = sys.argv[3]
    except IndexError:
        print('Usage: python server.py IP port audio_file')

    metodosposibles = ['INVITE', 'ACK', 'BYE']
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer((SERVIDOR, int(PUERTO)), EchoHandler)
    print("Listening...")
    serv.serve_forever()
