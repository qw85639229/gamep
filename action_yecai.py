# -*-encoding:utf-8-*-
import pyautogui
import time
import pyperclip

class Action_yecai(object):
    def __init__(self, windowLeftUp):
        self.windowLeftUp = windowLeftUp
        pyautogui.PAUSE = 0.005
        pyautogui.FAILSAFE = True
        self.timeTake = 6
        """Location"""
        self.buttonLocation = (244, 159)
        self.leftLocation = (211, 377)
        self.rightLocation = (1018, 438)
        self.resetLocation = (640,10)
        self.quitLocation = (1064,732)
        self.stripStartDrag = (787, 221)
        self.stripEndDrag = (786, 450)
        self.roomPassWordLocation = (646 , 387)
        self.roomPassWordEnterLocation = (583 , 472)
    def reLo(self, location):
        return (location[0] + self.windowLeftUp[0], location[1] + self.windowLeftUp[1])

    def basketball(self, data, type=0):
        if len(data) == 2:
            location1, location2 = data
            pyautogui.moveTo(location1)
            time.sleep(0.2)
            pyautogui.dragTo(x=location2[0], y=location2[1], duration=0.5, button='left')
            pyautogui.moveTo(location2)
            time.sleep(0.2)
        elif len(data) == 4:
            self.coverdbasketball(data, type)
        return

    def coverdbasketball(self, data, type=0):
        x, y, w, h = data
        location0, location1 = (x+5, y+5), (x+w-5, y+h-5)
        location2, location3 = (x+w-5, y+5), (x+5, y+h-5)
        (location_1, location_2) = [(location0, location1),
                                    (location1, location0),
                                    (location2, location3),
                                    (location3, location2)][type]
        pyautogui.moveTo(location_1)
        time.sleep(0.2)
        pyautogui.dragTo(x=location_2[0], y=location_2[1], duration=0.5, button='left')
        pyautogui.moveTo(location_2)
        time.sleep(0.2)
        return

    def wordMath(self, data):
        max_math_num, enterLocation, blankLocation = data
        pyautogui.moveTo(*blankLocation)
        time.sleep(0.2)
        pyautogui.click()
        time.sleep(0.2)
        pyautogui.press('backspace')
        time.sleep(0.2)
        pyautogui.press('backspace')
        time.sleep(0.2)
        pyautogui.typewrite(message=str(max_math_num), interval=0.5)
        time.sleep(0.2)
        pyautogui.moveTo(*enterLocation)
        time.sleep(0.2)
        pyautogui.click()
        time.sleep(0.2)
        pyautogui.moveTo(*self.reLo(self.resetLocation))
        time.sleep(0.2)
        return

    def wordHan(self, data):
        max_han_word, enterLocation, blankLocation = data
        pyautogui.moveTo(*blankLocation)
        time.sleep(0.2)
        pyautogui.click()
        time.sleep(0.2)
        pyautogui.press('backspace')
        time.sleep(0.2)
        pyautogui.press('backspace')
        time.sleep(0.2)
        pyperclip.copy(max_han_word)
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.2)
        pyautogui.moveTo(*enterLocation)
        time.sleep(0.2)
        pyautogui.click()
        time.sleep(0.2)
        pyautogui.moveTo(*self.reLo(self.resetLocation))
        time.sleep(0.2)
        return

    def rightArrow(self,data):
        rightArrowLocation, targetLocation = data
        pyautogui.moveTo(*rightArrowLocation)
        time.sleep(0.2)
        pyautogui.dragTo(x=targetLocation[0], y=targetLocation[1], duration=0.5, button='left')
        time.sleep(0.2)
        pyautogui.moveTo(*targetLocation)
        time.sleep(0.2)
        return

    def fish(self, rate):
        if rate > 1:
            pyautogui.keyDown('up')
            time_take = 0.5 if rate >= 1.7 else 0.2
            time.sleep(time_take)
            pyautogui.keyUp('up')
        else:
            pyautogui.keyDown('down')
            time_take = 0.5 if rate <= 0.4 else 0.2
            time.sleep(time_take)
            pyautogui.keyUp('down')

    def fishflag(self):
        pyautogui.moveTo(*self.reLo(self.buttonLocation))
        time.sleep(0.2)
        pyautogui.click()
        time.sleep(0.2)
        # print('点击钓鱼按钮')
        pyautogui.moveTo(self.reLo((100,100)))
        time.sleep(0.2)

    def dig(self,right=False):
        leftLocation = self.reLo(self.leftLocation)
        rightLocation = self.reLo(self.rightLocation)
        if right:
            action = rightLocation
        else:
            action = leftLocation

        pyautogui.moveTo(*action)
        time.sleep(0.05)
        pyautogui.click()
        time.sleep(0.05)
        pyautogui.rightClick()
        # time.sleep(self.timeTake)

    def click(self, location, right=False, relo=True):
        if relo:
            location = self.reLo(location)
        pyautogui.moveTo(location)
        time.sleep(0.2)
        if right:
            pyautogui.rightClick()
        else:
            pyautogui.click()
        time.sleep(0.2)

    def press(self, location):
        pyautogui.press(location)

    def move(self, location, timeTake=0.2, relo=True):
        location = self.reLo(location) if relo else location
        pyautogui.moveTo(location)
        time.sleep(timeTake)

    def drag(self, start, end, timetake=0.2):
        pyautogui.moveTo(self.reLo(start))
        pyautogui.dragTo(self.reLo(end),duration=timetake)

    def enterRoomPassword(self, pw):
        pyautogui.click(self.reLo(self.roomPassWordLocation))
        time.sleep(0.05)
        pyautogui.typewrite(message=pw,interval=0.4)
        pyautogui.click(self.reLo(self.roomPassWordEnterLocation))
        time.sleep(0.05)

    def leaveSnow1(self, lock):
        location1 = (632, 426)
        location2 = (879 , 194)
        lock.acquire()
        self.click(location1)
        lock.release()
        time.sleep(5)
        lock.acquire()
        self.click(location2)
        lock.release()
        time.sleep(5)
        return

    def leaveSnow2(self, lock):
        location1 = (535 , 413)
        location2 = (967 , 389)
        # location3 = (1081 , 306)
        location3 = (1091 , 112)
        for i in [location1,location2,location3]:
            lock.acquire()
            self.click(i)
            lock.release()
            time.sleep(5)

    def leaveSnow3(self, lock):
        location1 = (883 , 227)
        lock.acquire()
        self.click(location1)
        lock.release()
        time.sleep(10)

    def leaveSnow4(self, lock):
        location1 = (624, 493)
        location2 = (464 , 297)
        location3 = (258, 281)
        for i in [location1,location2, location3]:
            lock.acquire()
            self.click(i)
            lock.release()
            time.sleep(5)

    def leaveSnow(self,num, lock):
        function = [self.leaveSnow1,self.leaveSnow2,self.leaveSnow3,self.leaveSnow4,][num]
        function(lock)


    def reset(self):
        pyautogui.moveTo(self.reLo(self.resetLocation))
        time.sleep(0.2)
        pyautogui.click()
        time.sleep(0.2)
