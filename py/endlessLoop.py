#!/bin/python3
# coding: utf-8


#Date: Mon May 14 11:40:13 CST 2018
#Author: Zhang21
#Des: A endless loop script writed by python3 just for CPU test, analyze the high CPU usage and strace it, then find out the bug and debug.


import time, threading



def endless():
    print('Thread %s is running...' % threading.current_thread().name)
    i = 0
    while True:
        i += 1
        #time.sleep(1)
        print(i)

#多线程，如CPUs
def multi(cpus):
    for i in range(cpus):
        t =threading.Thread(target=endless)
        t.start()




multi(4)
