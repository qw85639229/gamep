# -*-encoding:utf-8-*-
import win32gui
import win32con
import time
import threading as th
from action_yecai import Action_yecai
from image_yecai import Image_yecai
import os
ifDebug = False

def print_dug(words):
    if ifDebug == True:
        print(words)


class AntYecai(object):
    def __init__(self, name= 'AntYecai', programPath='E:\\game\\AntYecaibuluo\\AntYecai.exe', test=False):
        print(time.strftime("%H_%M", time.localtime()), ": Start the program of AntYecai")
        self.name = name
        self.mode = None
        self.programPath = programPath
        self.allDayWork = [(5, 60 * 60 * 5), (0, 60 * 60 * 2.5), (2, 60 * 60 * 2), (3, -1)]
        self.lock_verify = th.Lock()
        hwnd = win32gui.FindWindow(None, name)
        if hwnd != 0:
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            print(f'Find location: left:{left}, top:{top}, right:{right}, bottom:{bottom}')
            self.windowLeftUp = (left,top)
            self.action = Action_yecai(self.windowLeftUp, self.lock_verify)
            self.image = Image_yecai(self.windowLeftUp)
        else:
            self.startProgram()
        self.verify_siuation = [": No verification",
                                ": Bastketball Check",
                                ": Enter a num",
                                ": Enter a han",
                                ": Right Arrow"]

        self.thread = []
        """Start StopSignal Thread"""
        self.stopSignal = False
        if not test:
            th.Thread(target=self.signalFunction, args=(), name='key_capture_thread', daemon=True).start()

        """Application Thread"""
        #verification
        if not test:
            self.verfiy_th = th.Thread(target=self.verifing)
            self.verfiy_th.start()
        #fishing
        self.fish_verify = False
        #eatingwithhunting
        self.div = []
        self.save_num = 20
        self.threshold_distance = 50**2
        self.forbinpoint = []
        #earn
        self.room_count = 0
        #hunting
        self.medicine_count = 0
        #dig
        self.dig_count = 0
        self.dig_type = 0

    def startProgram(self):
        hwnd = win32gui.FindWindow(None, self.name)
        if hwnd != 0:
            return
        os.startfile(self.programPath)
        time.sleep(2)
        hwnd = win32gui.FindWindow(None, self.name)
        win32gui.BringWindowToTop(hwnd)
        win32gui.SetForegroundWindow(hwnd)
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        time.sleep(2)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        self.windowLeftUp = (left, top)
        self.action = Action_yecai(self.windowLeftUp, self.lock_verify)
        self.image = Image_yecai(self.windowLeftUp)
        self.enterVillage()

    def enterVillage(self):
        self.action.click(self.action.startLocation, timeTake=1, iflock=False)
        self.action.click(self.action.pwenterLocation, timeTake=1, iflock=False)
        self.action.click(self.action.pwenterLocation2, timeTake=1, iflock=False)
        self.action.click(self.action.skipLocation, timeTake=1, iflock=False)
        self.action.reset(iflock=False)
        if self.mode != None:
            self.enterWorkArea(self.mode)

    def enterWorkArea(self, mode):
        while(self.image.checkBackGround() != 0):
            print_dug("Try to enter the start background")
            for i in range(2):
                time.sleep(0.1)
                if i == 0:
                    self.verify()
                img = [self.image.area_room_img, self.image.area_exit_img][i]
            # for img in [self.image.area_room_img, self.image.area_exit_img]:
            #     if img == self.image.area_room_img:
            #         self.verify()
                ret = self.image.checkImage(img)
                if ret != None:
                    self.action.click(ret[0], timeTake=1, iflock=False)
                    break
        if mode == 5: # Earn Snow with North
            self.action.click(self.action.newTownLocation, timeTake=1, iflock=False)
            ret = self.image.checkNotice()
            if ret != None:
                self.action.click(ret, timeTake=1, iflock=False)
        elif mode == 1: # Hunting
            self.action.click(self.action.huntLocation, timeTake=1, iflock=False)
            ret = self.image.checkNotice()
            if ret != None:
                self.action.click(ret, timeTake=1, iflock=False)
            self.action.CreatHuntRoom()
            time.sleep(2)
            roomtype = self.image.checkBackGround()
            if roomtype != 4:
                return
            self.verify()
            self.action.enterHuntWorkRoom()

        elif mode == 3 or mode == 0: # Eating with hunting && fishing
            self.action.click(self.action.homeTownLocation, timeTake=1, iflock=False)
            ret = self.image.checkNotice()
            if ret != None:
                self.action.click(ret, timeTake=1, iflock=False)
            circles = self.image.checkImage(self.image.area_fish_img)
            for circle in circles:
                print(circle)
                self.action.click(circle, iflock=False)
                self.action.reset(iflock=False)
                time.sleep(0.8)
                roomtype = self.image.checkBackGround()
                if roomtype == 4:
                    return
        elif mode == 2: # Diging
            self.action.click(self.action.homeTownLocation, timeTake=1, iflock=False)
            ret = self.image.checkNotice()
            if ret != None:
                self.action.click(ret, timeTake=1, iflock=False)
            self.action.CreatMineRoom()
            time.sleep(2)
            roomtype = self.image.checkBackGround()
            if roomtype != 4:
                return
            self.verify()
            self.action.enterMineWorkRoom()

    """
        Work Mode:
        0: Fish
        1: Hunting
        2: Diging
        3: Eating with hunting
        4: Earning
        5: Earn Snow with North
        """

    def verify(self):
        self.action.reset(iflock=False)
        self.startProgram()
        ret = self.image.checkNotice()
        if ret != None:
            self.action.click(ret, iflock=False)
        self.action.reset(iflock=False)
        situation, data = self.image.verify()
        if situation != 0:
            print(time.strftime("%H:%M:%S", time.localtime()), self.verify_siuation[situation])
        if situation == 0:
            return True
        self.fish_verify = True
        methods= [None, self.action.basketball, self.action.wordMath, self.action.wordHan, self.action.rightArrowPre]
        methods[situation](data)
        # print(f'situation = {situation}')
        if situation == 1:
            self.action.reset(iflock=False)
            if self.image.verify()[0] == 1:
                if len(data) == 2:
                    methods[situation](data[::-1])
                elif len(data) == 4:
                    for i in range(1,4):
                        methods[situation](data, type=i)
                        self.action.reset(iflock=False)
                        if not self.image.verify()[0] == 1:
                            break
        elif situation == 2:
            self.action.reset(iflock=False)
            time.sleep(2)
            ret = self.image.checkImage(self.image.enter_img)
            if ret != None:
                self.action.click(self.action.blankMath, iflock=False)
                self.action.press('backspace', iflock=False)
        elif situation == 3:
            self.action.reset(iflock=False)
            time.sleep(2)
            if self.image.verify()[0] == 3:
                self.action.click(self.action.blankHan,iflock=False)
                self.action.press('backspace',iflock=False)
        elif situation == 4:
            data = self.image.rightArrow(detect=False)
            self.action.rightArrow(data)
        return False

    def verifing(self, timeTake = 10):
        print("Verify Thread Start with timeTake = ", timeTake)
        while True:
            self.lock_verify.acquire()
            self.verify()
            self.lock_verify.release()
            time.sleep(timeTake)

    def signalFunction(self):
        print("Enter any to quit the Program")
        input()
        self.stopSignal = True
        return

    def mouseLocation(self):
        self.image.mouseLocation()

    def shoot(self,x,y,w,h,absolute= False, show=False):
        img = self.image.shoot(x,y,w,h,absolute, show)
        return img

    def fish(self):
        rate = self.image.fish()
        self.action.fish(rate)

    def fishflag(self):
        if self.fish_verify:
            self.fish_verify = False
            self.action.fishflag()
        if self.image.fishflag():
            print("Click to start fish")
            self.action.fishflag()

    def transfer(self, key='F2'):
        hp = self.image.checkHP()
        if hp > 0.8:
            self.action.press(key)

    def medicine(self, keys=[('F3', 10)]):
        for key, timeTake in keys:
            if self.medicine_count % timeTake == 0:
                self.lock_verify.acquire()
                self.action.press(key,iflock=False)
                time.sleep(0.1)
                location = self.image.checkNotice()
                if location != None:
                    self.action.click(location,iflock=False)
                self.lock_verify.release()
        self.medicine_count += 1
        if self.medicine_count >= 100:
            self.medicine_count = 0

    def hunt(self):
        ret = self.image.checkMonster()
        if ret != None:
            self.action.move(ret, timeTake=0.05)
            if self.image.checkMouse(ret) == 1:
                self.action.click(ret,right=False)


    def dig(self):
        # print('what dig ', self.image.checkHP())
        if self.image.checkHP() >= 0.2:
            self.action.dig(self.dig_type)
            self.dig_count += 1
            if self.dig_count >= 6:
                self.dig_count = 0
                self.dig_type += 1
            if self.dig_type >= 4:
                self.dig_type = 0
        else:
            time.sleep(0.2)

    def checkdiv(self):
        divret = self.image.div(6)
        return divret

    def eat(self, foodFirst=False):
        self.div = self.checkdiv()
        if self.div != None:
            food = []
            monster = []
            rubbish = []
            for x,y,w,h in self.div:
                middle_x = x + w // 2
                middle_y = y + h // 2
                self.action.move((middle_x, middle_y), 0.05)
                type_hand = self.image.checkMouse((middle_x, middle_y)) #0->food 1->monster 2->big rubbish
                if type_hand == 0:
                    food.append((middle_x,middle_y))
                    if foodFirst:
                        self.action.click((middle_x, middle_y))
                        time.sleep(15)
                        return
                if type_hand == 1:
                    monster.append((middle_x,middle_y))
                elif type_hand == 2:
                    rubbish.append((middle_x, middle_y))
                elif type_hand == 3:
                    self.forbinpoint.append((x,y,w,h))
            if len(rubbish) > 0:
                self.action.click(rubbish[0],right=False)
                time.sleep(2)
                return
            if len(monster) > 0:
                self.action.click(monster[0], right=False)
                time.sleep(2)
                return
            if len(food) > 0:
                self.action.click(food[0],right=False)
                time.sleep(5)
                return
    def earn(self):
        roomtype = self.image.checkBackGround() # 0->start 1->new 2->hunt 3->hometown 4->room
        print('what',roomtype)
        if roomtype == 4:
            print("There is Room and quit")
            self.action.click(self.action.quitLocation)
            return
        if roomtype == 3:
            circles = self.image.checkRoomCircle()
            print(f'There is HomeTown and find {len(circles)} circles')
            if len(circles) <= 0:
                print("NO circles")
                return
            if self.room_count >= len(circles):
                self.room_count = 0
            # enter the room
            print(f'Enter the room {self.room_count}')
            self.action.click(circles[self.room_count])
            self.action.reset()
            time.sleep(0.8)
            roomtype = self.image.checkBackGround()
            if roomtype != 4:
                self.room_count += 1
                print('Fail to enter the room')
                ret = self.image.checkNotice()
                if ret != None:
                    print("Find Notice")
                    self.action.click(ret)
                return
            #successfully enter the room
            #check food and rubbish
            food_rubbish_locations = self.image.checkFoodRubbish(food=True,rubbish=True)
            print(f"Find {len(food_rubbish_locations)} food and rubbish")
            for location in food_rubbish_locations:
                self.action.move(location, 0.05)
                handtype = self.image.checkMouse(location)
                if handtype != 0:
                    # print("Error with hand type: ", handtype)
                    continue
                self.action.click(location)
                time.sleep(2)
            print('Finish collecting and quit the room')
            #quit the room
            self.action.click(self.action.quitLocation)
            self.room_count += 1

    def findGetFoodRubbish(self, food=True, rubbish=True, timeTake=2):
        food_rubbish_locations = self.image.checkFoodRubbish(food=food, rubbish=rubbish)
        for location in food_rubbish_locations:
            self.action.move(location, 0.05)
            handtype = self.image.checkMouse(location)
            if handtype != 0:
                # print("Error with hand type: ", handtype)
                continue
            self.action.click(location)
            time.sleep(timeTake)
        return

    def earnSnowNorth(self):
        roomtype = self.image.checkBackGround()
        roomType = ['start', 'new', 'hunt', 'hometown', 'room','snow2','snow3','snow4','snow5']
        print_dug(f'Find Room Type: {roomType[roomtype]}')
        if roomtype >= 4:
            print_dug("There is Room and quit")
            self.action.click(self.action.quitLocation)
            return
        elif roomtype == 1:
            self.action.drag(self.action.stripStartDrag, self.action.stripEndDrag)
            circles = self.image.checkRoomCaomei()
            print_dug(f'There is HomeTown and find {len(circles)} circles')
            if len(circles) <= 0:
                print_dug("NO circles")
                return
            if self.room_count >= len(circles):
                self.room_count = 0
            # enter the room
            print_dug(f'Enter the room {self.room_count}')
            self.action.click(circles[self.room_count])
            time.sleep(0.5)
            self.action.enterRoomPassword('110119')
            self.action.reset()
            time.sleep(2)

            roomtype = self.image.checkBackGround()
            if roomtype != 4:
                self.room_count += 1
                print_dug('Fail to enter the room')
                ret = self.image.checkNotice()
                if ret != None:
                    print_dug("Find Notice")
                    self.action.click(ret)
                return

            # Snow areas has 5 area
            # now we are in the first one
            # food_rubbish_locations = self.image.checkFoodRubbish(food=True, rubbish=True)
            # successfully enter the room
            # check food and rubbish
            self.findGetFoodRubbish()
            for i in range(4):
                self.action.leaveSnow(i)
                self.action.reset()
                success_flag = False
                for j in range(2):
                    if self.image.checkBackGround(checksnow=True) != i + 5:
                        print_dug(f"Leave snow{i} Fail! It's ")
                        self.action.leaveSnow(i)
                        self.action.reset()
                    else:
                        success_flag = True
                        break
                if success_flag == False:
                    self.action.click(self.action.quitLocation)
                    self.room_count += 1
                    return
                self.findGetFoodRubbish()
            self.action.click(self.action.quitLocation)
            self.room_count += 1

    def appThread(self, function, timeTake=0):
        while not self.stopSignal:
            function()
            if timeTake > 0:
                time.sleep(timeTake)

    def start(self, mode= 0, ewa=False):
        self.mode = mode
        self.thread = []
        if mode in [0,1,2,3,5] and ewa:
            self.lock_verify.acquire()
            self.enterWorkArea(mode)
            self.lock_verify.release()
        workmode = [
            [(self.fishflag, 30), (self.fish, 0)],
            [(self.hunt, 20), (self.transfer, 20), (self.medicine, 60)],
            [(self.dig, 4)],
            [(self.eat, 0),(self.transfer, 20)],
            [(self.earn, 0)],
            [(self.earnSnowNorth, 0)]][mode]

        theThread = self.appThread

        for work, timeTake in workmode:
            self.thread.append(th.Thread(target=theThread, args=(work, timeTake)))
            print(work.__name__, " Thread Start with timeTake = ", timeTake)

        for thread in self.thread:
            thread.start()

    def allDay(self):
        restTime = 60 * 60 * 24
        for work, timeTake in self.allDayWork:
            self.stopSignal = False
            print(f"Start work {self.allDayWork[0]}")
            self.start(work, ewa=True)
            if timeTake > 0:
                restTime = restTime - timeTake
                time.sleep(timeTake)
            else:
                time.sleep(restTime)
            self.stopSignal = True
            print(f"Start to stop work {self.allDayWork[0]}")
            for i in self.thread:
                i.join()
        print('finish')

    def deamon(self):
        curday = time.localtime().tm_mday
        print("Deamon start at ", curday)
        while(time.localtime().tm_mday == curday):
            time.sleep(60 * 20)
        self.stopSignal = True
        print(f"Start to stop Tmpwork {self.allDayWork[0]}")
        for i in self.thread:
            i.join()
        while True:
            self.allDay()


if __name__ == '__main__':
    print('*' * 20)
    # time.sleep(2)
    program = AntYecai(test=False)
    program.mouseLocation()
    # program.allDay()
    # program.start(1,ewa=True)
    # program.deamon()
    # print(
    #     """
    # Work Mode:
    # 0: Fish
    # 1: Hunting
    # 2: Diging
    # 3: Eating with hunting
    # 4: Earning
    # 5: Earn Snow with North
    # """
    # )
    # program.start(2)


    # rubbish
    # program = AntYecai(test=False)
    # program.mouseLocation()
    # rubbishMan = (576, 283)
    # rubbishUp = (734, 376)
    # rubbishExchange = (574, 470)
    # rubbishStop = [(467, 444),(569, 449),(683, 444)]
    # #click rubbish man
    # while True:
    #     program.action.click(rubbishMan)
    #     #click rubbish up
    #     for i in range(3):
    #         program.action.click(rubbishUp)
    #         time.sleep(0.05)
    #     #exchange
    #     program.action.click(rubbishExchange)
    #     time.sleep(0.1)
    #     for i in range(3):
    #         program.action.click(rubbishStop[i])
    #         time.sleep(0.2)
    #     time.sleep(8)

    #bubble wrap
    # while True:
    #     time.sleep(0.5)
    #     program.action.press('F9')
    #     time.sleep(0.5)
    #     program.action.bubblewrap()
    #     time.sleep(0.5)
    #     program.action.click(program.action.pwenterLocation2)

    #test
    # import numpy as np
    # import cv2
    # background = program.image.shoot(*program.image.backgroundLocation)
    # x_length = [170, 1120]
    # y_length = [40, 670]
    # map_img = np.zeros(background.shape, dtype=np.uint8)
    # """
    # walk area: white (255,255,255)
    # door area: brown (135,184,222)
    # forbidden area: yellow (0,255,255)
    # """
    # mouseTotalType = [-1, 0, 1, 2, 3]
    # mapColor = [(0,0,0),       # black
    #             (255,255,255), # white
    #             (135,184,222), # brown
    #             (0,255,255)]   # yellow
    # cell_length = 40
    # for x in range(x_length[0],x_length[1], cell_length):
    #     for y in range(y_length[0],y_length[1],cell_length):
    #         program.action.move((x+cell_length//2, y+cell_length//2), timeTake=0.1, iflock=False)
    #         mousetype = program.image.checkMouse((x+cell_length//2, y+cell_length//2))
    #         for i in range(5):
    #             if mousetype != mouseTotalType[i]:
    #                 continue
    #             if i == 0:
    #                 map_img[y:y+cell_length,x:x+cell_length,:] = list(mapColor[2])
    #             elif 0 < i < 4:
    #                 map_img[y:y + cell_length, x:x + cell_length, :] = list(mapColor[1])
    #             elif i == 4:
    #                 map_img[y:y + cell_length, x:x + cell_length, :] = list(mapColor[3])
    #
    # cv2.imshow('r',map_img)
    # cv2.waitKey()