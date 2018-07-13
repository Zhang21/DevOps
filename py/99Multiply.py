#!/bin/python3
# _*_: coding: utf-8 _*_


for i in range(1, 10):
    for j in range(i, 10):
        print('{} * {} = {:2}'.format(i, j, (i * j)))
    print('')
