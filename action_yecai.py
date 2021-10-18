# -*-encoding:utf-8-*-
import pyautogui
import time
import pyperclip

class Action_yecai(object):
    def __init__(self, windowLeftUp, lock):
        self.windowLeftUp = windowLeftUp
        pyautogui.PAUSE = 0.005
        pyautogui.FAILSAFE = True
        self.lock = lock
        self.timeTake = 6
        self.snowTimeTake = 1.5
        """Location"""
        self.startLocation = (654, 396)
        self.pwenterLocation = (620,493)
        self.pwenterLocation2 = (656,485)
        self.skipLocation = (1081, 110)

        self.buttonLocation = (244, 159)
        self.rightArrowRight = (757,449)
        self.blankHan = (606 , 421)

        self.leftLocation = (443 , 353)
        self.rightLocation = (869 , 353)
        self.leftDownLocation = (438 , 544)
        self.rightDownLocation = (869 , 553)

        self.resetLocation = (640,10)
        self.quitLocation = (1064,732)
        self.stripStartDrag = (787, 221)
        self.stripEndDrag = (786, 450)
        self.roomPassWordLocation = (646 , 387)
        self.roomPassWordEnterLocation = (583 , 472)

        self.homeTownLocation = (308 , 469)
        self.newTownLocation = (655, 468)
        self.huntLocation = (253 , 181)

        self.createRoom = (725 , 77)
        self.createPrivateButtion = (635 , 238)
        self.createPrivatePW = (779 , 236)
        self.createButtion = (915 , 203)
        self.dragMap = [(969 , 351), (969 , 459)]
        self.mineMap = (419 , 547)
        self.huntMap = (410 , 410)

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
        gap = 20
        location0, location1 = (x+gap, y+gap), (x+w-gap, y+h-gap)
        location2, location3 = (x+w-gap, y+gap), (x+gap, y+h-gap)
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
        max_han_word, enterLocation = data
        pyautogui.moveTo(*self.reLo(self.blankHan))
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

    def rightArrowPre(self, data):
        rightArrowLocation = data
        pyautogui.moveTo(*rightArrowLocation)
        pyautogui.mouseDown(x=rightArrowLocation[0], y=rightArrowLocation[1], button='left')
        pyautogui.moveTo(*self.reLo(self.rightArrowRight),duration=0.4)
        return

    def rightArrow(self,data):
        print(f'move to ({data[0]}, {data[1]})')
        pyautogui.moveTo(*data, duration=0.5)
        pyautogui.mouseUp(x=data[0], y=data[1], button='left', duration=0.1)
        # rightArrowLocation, targetLocation = data
        # pyautogui.moveTo(*rightArrowLocation)
        # time.sleep(0.2)
        # pyautogui.dragTo(x=targetLocation[0], y=targetLocation[1], duration=0.5, button='left')
        # time.sleep(0.2)
        # pyautogui.moveTo(*targetLocation)
        # time.sleep(0.2)
        return

    def fish(self, rate):
        if rate > 1:
            self.lock.acquire()
            pyautogui.keyDown('up')
            self.lock.release()
            time_take = 0.5 if rate >= 1.7 else 0.2
            time.sleep(time_take)
            self.lock.acquire()
            pyautogui.keyUp('up')
            self.lock.release()
        else:
            self.lock.acquire()
            pyautogui.keyDown('down')
            self.lock.release()
            time_take = 0.5 if rate <= 0.4 else 0.2
            time.sleep(time_take)
            self.lock.acquire()
            pyautogui.keyUp('down')
            self.lock.release()

    def fishflag(self):
        self.lock.acquire()
        pyautogui.moveTo(*self.reLo(self.buttonLocation))
        time.sleep(0.05)
        pyautogui.click()
        time.sleep(0.05)
        # print('点击钓鱼按钮')
        pyautogui.moveTo(self.reLo((100,100)))
        time.sleep(0.05)
        self.lock.release()

    def dig(self,type=0):
        leftLocation = self.reLo(self.leftLocation)
        rightLocation = self.reLo(self.rightLocation)
        leftdownLocation = self.reLo(self.leftDownLocation)
        rightdownLocation = self.reLo(self.rightDownLocation)

        action = [leftLocation, leftdownLocation, rightdownLocation, rightLocation][type]
        self.lock.acquire()
        pyautogui.moveTo(*action)
        time.sleep(0.05)
        pyautogui.click()
        time.sleep(0.05)
        pyautogui.moveTo(self.reLo((640,100)))
        time.sleep(0.05)
        pyautogui.rightClick()
        time.sleep(0.05)
        self.lock.release()
        # time.sleep(self.timeTake)

    def bubblewrap(self):
        """
        bubblewrap has 10 * 9 bubbles
        :return:
        """
        bubbleLeftUp = self.reLo((482 , 236))
        bubbleRightDown = self.reLo((818, 615))
        nextbubbleX = self.reLo((524 , 236))
        nextbubbleY = self.reLo((482 , 281))
        cell_w = nextbubbleX[0] - bubbleLeftUp[0]
        cell_h = nextbubbleY[1] - bubbleLeftUp[1]

        self.move(bubbleLeftUp, relo=False)
        pyautogui.mouseDown(x=bubbleLeftUp[0], y=bubbleLeftUp[1], button='left')
        startLocation = bubbleLeftUp
        endLocation = bubbleRightDown
        for i in range(4):
            """Down"""
            self.move((startLocation[0],endLocation[1]), duration=0.5, timeTake=0, relo=False)
            """Right"""
            self.move((endLocation[0], endLocation[1]), duration=0.4, timeTake=0, relo=False)
            """Up"""
            self.move((endLocation[0], startLocation[1]), duration=0.5, timeTake=0, relo=False)
            """Left"""
            self.move((startLocation[0] + cell_w, startLocation[1]), duration=0.6, timeTake=0.1, relo=False)
            """Reset"""
            startLocation = (startLocation[0] + cell_w, startLocation[1] + cell_h)
            endLocation = (endLocation[0] - cell_w, endLocation[1] - cell_h)
            self.move(startLocation,duration=0.1, timeTake=0, relo=False)
        endLocation = (bubbleLeftUp[0] + 4 * cell_w,bubbleLeftUp[1] + 5 * cell_h)
        self.move(endLocation, duration=0.4, relo=False)
        pyautogui.mouseUp(x=endLocation[0], y=endLocation[1], button='left')
        # pyautogui.moveTo(*self.reLo(self.rightArrowRight), duration=0.4)


    def click(self, location, timeTake=0.05, right=False, relo=True, iflock=True):
        if relo:
            location = self.reLo(location)
        if iflock:
            self.lock.acquire()
        pyautogui.moveTo(location)
        time.sleep(timeTake)
        if right:
            pyautogui.rightClick()
        else:
            pyautogui.click()
        time.sleep(timeTake)
        if iflock:
            self.lock.release()

    def press(self, location, iflock=True):
        if iflock:
            self.lock.acquire()
        pyautogui.press(location)
        if iflock:
            self.lock.release()

    def move(self, location, timeTake=0.2, duration=0., relo=True, iflock=True):
        if iflock:
            self.lock.acquire()
        location = self.reLo(location) if relo else location
        pyautogui.moveTo(location,duration=duration)
        time.sleep(timeTake)
        if iflock:
            self.lock.release()

    def drag(self, start, end, timetake=0.2,  iflock=True):
        if iflock:
            self.lock.acquire()
        pyautogui.moveTo(self.reLo(start))
        pyautogui.dragTo(self.reLo(end),duration=timetake)
        if iflock:
            self.lock.release()

    def enterRoomPassword(self, pw, iflock=True):
        if iflock:
            self.lock.acquire()
        pyautogui.click(self.reLo(self.roomPassWordLocation))
        time.sleep(0.05)
        pyautogui.typewrite(message=pw,interval=0.4)
        pyautogui.click(self.reLo(self.roomPassWordEnterLocation))
        time.sleep(0.05)
        if iflock:
            self.lock.release()


    def leaveSnow1(self):
        location1 = (632, 426)
        location2 = (879 , 194)
        self.click(location1)
        time.sleep(self.snowTimeTake)
        self.click(location2)
        time.sleep(self.snowTimeTake)
        return

    def leaveSnow2(self):
        location1 = (535 , 413)
        location2 = (967 , 389)
        # location3 = (1081 , 306)
        location3 = (1091 , 112)
        for i in [location1,location2,location3]:
            self.click(i)
            time.sleep(self.snowTimeTake)

    def leaveSnow3(self):
        location1 = (728, 405)
        location2 = (883 , 227)
        # location2 = (728 , 405)
        for i in [location1, location2]:
            self.click(i)
            time.sleep(self.snowTimeTake)

    def leaveSnow4(self):
        location1 = (624, 493)
        location2 = (464 , 297)
        location3 = (258, 281)
        for i in [location1,location2, location3]:
            self.click(i)
            time.sleep(self.snowTimeTake)

    def leaveSnow(self,num):
        function = [self.leaveSnow1,self.leaveSnow2,self.leaveSnow3,self.leaveSnow4,][num]
        function()

    def CreatMineRoom(self, pw='110119'):
        self.click(self.createRoom, timeTake=1, iflock=False)
        self.click(self.createPrivateButtion, timeTake=1, iflock=False)
        self.click(self.createPrivatePW, timeTake=1, iflock=False)
        pyautogui.typewrite(message=pw,interval=0.2)
        self.move(self.dragMap[0], iflock=False)
        pyautogui.dragTo(self.reLo(self.dragMap[1]), duration=0.5)

        self.click(self.mineMap, timeTake=1, iflock=False)
        self.click(self.createButtion, timeTake=1, iflock=False)
        return

    def enterMineWorkRoom(self, timeTake=4):
        location1 = (1100 , 519)
        location2 = (689 , 147)
        location3 = (219 , 277)
        for i in [location1, location2, location3]:
            self.click(i, iflock=False)
            time.sleep(timeTake)

    def CreatHuntRoom(self, pw='110119'):
        self.click(self.createRoom, timeTake=1, iflock=False)
        self.click(self.createPrivateButtion, timeTake=1, iflock=False)
        self.click(self.createPrivatePW, timeTake=1, iflock=False)
        pyautogui.typewrite(message=pw,interval=0.2)
        # self.move(self.dragMap[0], iflock=False)
        # pyautogui.dragTo(self.reLo(self.dragMap[1]), duration=0.5)

        self.click(self.huntMap, timeTake=1, iflock=False)
        self.click(self.createButtion, timeTake=1, iflock=False)
        return

    def enterHuntWorkRoom(self, timeTake=4):
        location1 = (1067 , 653)
        for i in range(5):
            self.click(location1, iflock=False)
            time.sleep(timeTake)

    def reset(self, iflock=True):
        if iflock:
            self.lock.acquire()
        pyautogui.moveTo(self.reLo(self.resetLocation))
        time.sleep(0.05)
        pyautogui.click()
        time.sleep(0.05)
        if iflock:
            self.lock.release()
