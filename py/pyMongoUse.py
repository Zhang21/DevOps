#!/bin/python3
# -*- coding: utf-8 -*-

'''
Learn to use pyMongo

    pyMongo docs: <https://api.mongodb.com/python/current/>
    A basic example is as follows.
'''

__author__ = 'Zhang21'

import pymongo
import pprint

mongoHost = 'localhost'
mongoPort = 27017
mongoUser = 'username'
mongoPassword = 'password'

client = pymongo.MongoClient(host=mongoHost, port=mongoPort, username=mongoUser, password=mongoPassword)
db = client.testDB
collection = db.testCollection


#插入实例
post = {
  '_id': 'test',
  'title': 'test',
  'text': 'test insert',
  'date': '2018-06-14'
}

try:
    collection.insert_one(post)
except pymongo.errors.DuplicateKeyError:
    print('Already posted!')
else:
    print('post!')
finally:
    pprint.pprint(collection.find_one({'_id': 'test'}))
