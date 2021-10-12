import threading
import time
lock = threading.Lock()
def test1():
    for i in range(5):
        lock.acquire()
        print('test1a: ', i)

        print('test1b: ', i)
        time.sleep(0.5)
        print('test1c: ', i)
        time.sleep(0.5)
        lock.release()
        time.sleep(5)

def test2():
    for i in range(5):
        lock.acquire()
        print('test2: ', i)
        time.sleep(0.5)
        lock.release()
        time.sleep(2)

if __name__ == '__main__':
    a = threading.Thread(target=test1)
    b = threading.Thread(target=test2)
    a.start()
    b.start()

