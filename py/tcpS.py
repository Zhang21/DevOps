#!/bin/bash
# -*- coding: utf-8 -*-

'''
    Just a test about socket web program.
    server-side
'''

import socket

host = 'localhost'
port = 5678
bf = 1024
maxConn = 3

tcpS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpS.bind((host, port))
tcpS.listen(maxConn)

print('Server start at {host}:{port}'.format(host=host, port=port))
print('Waiting for connection...')

while True:
    conn, addr = tcpS.accept()
    print('Connected by: {addr}'.format(addr=addr))

    while True:
        data = conn.recv(bf)
        print(data.decode('utf-8'))
        conn.send('server received message.'.encode('utf-8'))
    tcpS.close()



