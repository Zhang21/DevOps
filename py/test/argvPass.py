#!/usr/bin/python3
# -*- coding: utf-8 -*-



'''
Date: Tue May 15 11:19:31 CST 2018
Author: Zhang21
Des: Arguement Passing
'''


import sys


num = len(sys.argv)

if num != 3:
    print('Usage: xxx.py argv1 argv2')
else:
    print('argu[0] is ' + sys.argv[0])
    print('argu[1] is ' + sys.argv[1])
    print('argu[2] is ' + sys.argv[2])
