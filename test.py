import win32gui
import win32con
import time
import threading as th
import os
import time
import numpy as np


def test_th(arg=None):
    time.sleep(5)

thread_container = []
for i in range(5):
    thread_container.append(th.Thread(target=test_th, name=str(i)))

print(th.active_count())
for thread in thread_container:
    thread.start()
print(th.active_count())