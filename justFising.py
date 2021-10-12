import cv2
import time
import pyautogui
import numpy as np
pyautogui.PAUSE = 0.001
def fish():
    fishLeftUp = (698 , 310)
    fishRightDown = (fishLeftUp[0]+14, fishLeftUp[1] + 75)
    fish_img = pyautogui.screenshot(region=(*fishLeftUp, 14, 75))
    fish_img = np.array(fish_img)[:,:,[2,1,0]]
    fish_img = cv2.cvtColor(fish_img, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite('img/fishstrip.png', fish_img)
    # fish_img = cv2.adaptiveThreshold(fish_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 1)
    # cv2.imshow('test',fish_img)
    # cv2.waitKey()
    # exit()
    fish_strip = fish_img[:, fish_img.shape[1] // 2]
    min_fish_strip_index = np.argmin(fish_strip)
    if min_fish_strip_index > fish_img.shape[0] // 2:
        pyautogui.keyDown('up')
        print(min_fish_strip_index/(fish_img.shape[0]//2),'up')
        time_take = 0.5 if min_fish_strip_index/(fish_img.shape[0]//2) >= 1.7 else 0.2
        if min_fish_strip_index/(fish_img.shape[0]//2) >= 1.7:
            print('special situation, need more up')
        time.sleep(time_take)
        pyautogui.keyUp('up')
    else:
        pyautogui.keyDown('down')
        print(min_fish_strip_index/(fish_img.shape[0]//2),'down')
        time_take = 0.5 if min_fish_strip_index / (fish_img.shape[0] // 2) <= 0.3 else 0.2
        if min_fish_strip_index/(fish_img.shape[0]//2) <= 0.3:
            print('special situation, need more down')
        time.sleep(time_take)
        pyautogui.keyUp('down')



if __name__ == '__main__':
    time.sleep(3)
    while True:
        fish()
