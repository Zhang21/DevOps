#!/bin/python3
# -8- coding: utf-8 -8-

import time, threading

print('thread start.')

def wakeup(times):
    time.sleep(5)
    n=times
    for i in range(n):
        print('Wake UP!')

thread02 = threading.Thread(target=wakeup, args=[3])
thread02.start()

print('End of program!')
