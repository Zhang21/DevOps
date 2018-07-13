#!/bin/python3
# -*- coding: utf-8 -*-

'''
    Just a udp program
    Client-side
    And store the message to MongoDB.
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
mongoColl = 'udpC'

udpC = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
collection = MongoClient(host=host, port=mongoPort, \
             username=mongoUser, password=mongoPw).zhang.udpC


while True:
    msg = str(input('Please input message: \n'))
    udpC.sendto(msg.encode('utf-8'), (host, port))
    data = udpC.recv(bf)
    print(data.decode('utf-8'))

    dateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    post = {
      'author': 'Client',
      'date': dateTime,
      'message': data.decode('utf-8')
    }
    collection.insert_one(post)

    udpC.close()

