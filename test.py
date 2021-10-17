import win32gui
import win32con
import time
import threading as th
import os
import time
import numpy as np

a = time.localtime().tm_mday
print(a)

def deamon():
    cur_time = time.localtime().tm_min
    print("Program start at ", cur_time)
    while(time.localtime().tm_min <= cur_time):
        print('wait for 10 second')
        time.sleep(10)

    print("Program end at", time.localtime().tm_min)

deamon()