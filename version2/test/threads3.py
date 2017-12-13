#!/usr/bin/python

import threading
import time
import random

exitFlag = 0
my_list = [1, 2, 3, 4, 5, 6]

def get_data(lock):
  print('Starting get_data Thread')
  while True:
    lock.acquire()
    try:
      my_list.append(random.randint(0, 100))
      time.sleep(5)
    finally:
      lock.release()
    time.sleep(10)
  return

def serve_data(lock):
  num_tries = 0
  print('Starting serve_data Thread')
  while True:
    time.sleep(1)
    acquired = lock.acquire(0)
    try:
      num_tries += 1
      if acquired:
        print "lock acquired after " + str(num_tries) + " attempts"
        print(my_list)
        num_tries = 0
      else:
        print "data locked"
    finally:
      if acquired:
        lock.release()


if __name__ == '__main__':
  lock = threading.Lock()
  
  get_d = threading.Thread(target=get_data, args=(lock,), name='Get Data')
  get_d.setDaemon(True)
  get_d.start()


  serve_d = threading.Thread(target=serve_data, args=(lock,), name='Serve Data')
  serve_d.start()
