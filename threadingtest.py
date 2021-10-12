import threading
import time
lock = threading.Lock()
def test1():
    for i in range(5):
        lock.acquire()
        print('test1: ', time.strftime("%H:%M:%S", time.localtime()))
        lock.release()
        time.sleep(5)

def test2():
    for i in range(250):
        lock.acquire()
        y = 1 + 623
        time.sleep(0.1)
        # print('test2: ', time.strftime("%H:%M:%S", time.localtime()))
        lock.release()
        # time.sleep(2)
        # time.sleep(0.1)
if __name__ == '__main__':
    print('Start: ', time.strftime("%H:%M:%S", time.localtime()))
    a = threading.Thread(target=test1)
    b = threading.Thread(target=test2)
    a.start()
    b.start()
    a.join()
    b.join()
    print('End: ', time.strftime("%H:%M:%S", time.localtime()))
