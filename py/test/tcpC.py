#!/bin/python3
# -*- coding: utf-8 -*-

'''
    Just a test about socket program.
    Client-side
'''

import socket

host = 'localhost'
port = 5678
bf = 1024

tcpC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpC.connect((host, port))

while True:
    msg = input('Please input message: \n')
    tcpC.send(msg.encode('utf-8'))
    data = tcpC.recv(bf)
    print(data.decode('utf-8'))
