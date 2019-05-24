'''Learn multiprocess 

    Learn multiprocess of python.
'''

import os
import time
import random
from multiprocessing import Process, Queue


"""
# singe process
def long_time_task():
    print('当前进程: {}'.format(os.getpid()))
    time.sleep(2)
    print('结果: {}'.format(8 ** 20))

if __name__ == "__main__":
    print('当前母进程: {}'.format(os.getpid()))
    start = time.time() 
    for i in range(2):
        long_time_task()
    end = time.time()
    print('用时: {}s'.format((end - start)))
"""

"""
# multiprocess
def long_time_task(i):
    print("子进程: {} - 任务{}".format(os.getpid(), i))
    time.sleep(2)
    print("结果: {}".format(8 ** 20))

if __name__ == '__main__':
    print('当前母进程: {}'.format(os.getpid()))
    start = time.time()
    p1 = Process(target=long_time_task, args=(1,))    
    p2 = Process(target=long_time_task, args=(2,))
    print('等待所有子进程完成!')
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    end = time.time()
    print('总用时: {} s'.format((end - start)))
"""

# share data with multiprocess
# 2 process, one for write, one for read. Implemented sharing a queue
def write(q):
    print('进程写: {}'.format(os.getpid())) 
    for value in ['A', 'B', 'C']:
        print('将 {} 放入队列...'.format(value))
        q.put(value)
        time.sleep(random.random())

def read(q):
    print('进程读: {}'.format(os.getpid()))
    while True:
        value = q.get(True)
        print('从队列获取 {}'.format(value))

if __name__ == '__main__':
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    pw.start()
    pr.start()
    # 等待pw结束
    pw.join()
    # pr进程里是死循环，无法等待其结束，只能强行终止
    pr.terminate()

