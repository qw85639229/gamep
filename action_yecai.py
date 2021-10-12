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

    def dig(self,count):
        leftLocation = self.reLo(self.leftLocation)
        rightLocation = self.reLo(self.rightLocation)
        if count // 6 % 2 == 1:
            action = rightLocation
        else:
            action = leftLocation

        pyautogui.moveTo(*action)
        time.sleep(0.1)
        pyautogui.click()
        time.sleep(0.1)
        pyautogui.rightClick()
        time.sleep(self.timeTake)

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

    def move(self, location, timeTake, relo=True):
        location = self.reLo(location) if relo else location
        pyautogui.moveTo(location)
        time.sleep(timeTake)

    def reset(self):
        pyautogui.moveTo(self.reLo(self.resetLocation))
        time.sleep(0.2)
        pyautogui.click()
        time.sleep(0.2)
