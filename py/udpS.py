#!/bin/python3
# -*- coding: utf-8 -*-

'''
    Just a udp socket program
    Server-side
    And store the message to mongoDB.
'''

from pymongo import MongoClient
import socket, datetime


host = 'localhost'
port = 5679
bf = 1024

mongoPort = 27017
mongoUser = 'zhang'
mongoPw = 'password'
mongoDb = 'zhang'
mongoColl = 'udpS'

udpS = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpS.bind((host, port))

collection = MongoClient(host=host, port=mongoPort, \
             username=mongoUser, password=mongoPw).zhang.udpS

print('udp socket on {host}:{port}...'.format(host=host, port=port))


while True:
    data, addr = udpS.recvfrom(bf)
    print('Received from {addr}'.format(addr=addr))
    print(data.decode('utf-8'))
    print('\n')

    msg = 'Server has recived!\n'
    udpS.sendto(msg.encode('utf-8'), addr)

    dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    post = {
      'author': 'Server',
      'date': dateTime,
      'message': data.decode('utf-8')
    }
    collection.insert_one(post)
