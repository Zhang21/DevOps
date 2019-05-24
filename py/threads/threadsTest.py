'''learn multiThreads

    Learn multiThreads of python.
'''

import time, random, threading
from queue import Queue


"""
def long_time_task(i):
    print('当前子线程: {}, 任务: {}'.format(threading.current_thread().name, i))
    time.sleep(2)
    print('结果: {}'.format(8 ** 20))

if __name__ == '__main__':
    start = time.time()
    print('主线程: {}'.format(threading.current_thread().name))
    t1 = threading.Thread(target=long_time_task, args=(1,))
    t2 = threading.Thread(target=long_time_task, args=(2,))
    t1.start()
    t2.start()
    end = time.time()
    print('总用时: {}s'.format((end - start)))
"""


# 使用queue队列通信-经典的生产者和消费者模型
# 一个负责生成，一个负责消费，所生成的产品存放在queue里，实现了不同线程间沟通
# Producer
class Producer(threading.Thread):
    def __init__(self, name, queue):
        threading.Thread.__init__(self, name=name)
        self.queue = queue
    
    def run(self):
        for i in range(1, 5):
            print('{} 生产 {} 到队列'.format(self.getName(), i))
            self.queue.put(i)
            time.sleep(random.randrange(10) / 5)
        print('{} 完成!'.format(self.getName()))

# Consumer
class Consumer(threading.Thread):
    def __init__(self, name, queue):
        threading.Thread.__init__(self, name=name)
        self.queue = queue

    def run(self):
        for i in range(1, 5):
            val = self.queue.get()
            print('{} 消费队列中的 {}'.format(self.getName(), val))
            time.sleep(random.randrange(10))
        print('{} 完成!'.format(self.getName()))

def main():
    queue = Queue()
    producer = Producer('Producer', queue)
    consumer = Consumer('Consumer', queue)
    producer.start()
    consumer.start()
    producer.join()
    consumer.join()
    print('所有线程已完成!')

if __name__ == "__main__":
    main()
