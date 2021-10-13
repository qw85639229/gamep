# -*-encoding:utf-8-*-
import win32gui
import time
import threading as th
from action_yecai import Action_yecai
from image_yecai import Image_yecai

class AntYecai(object):
    def __init__(self, name= 'AntYecai', test=False):
        print(time.strftime("%H_%M", time.localtime()), ": Start the program of AntYecai")
        hwnd = win32gui.FindWindow(None, name)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        print(f'Find location: left:{left}, top:{top}, right:{right}, bottom:{bottom}')
        self.windowLeftUp = (left,top)
        self.action = Action_yecai(self.windowLeftUp)
        self.image = Image_yecai(self.windowLeftUp)
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
        self.lock_verify = th.Lock()
        self.lock_app = th.Lock()
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
        #dig
        self.dig_count = 0

    def verify(self):
        self.action.reset()
        situation, data = self.image.verify()
        if situation != 0:
            print(time.strftime("%H:%M:%S", time.localtime()), self.verify_siuation[situation])
        if situation == 0:
            return True
        self.fish_verify = True
        methods= [None, self.action.basketball, self.action.wordMath, self.action.wordHan, self.action.rightArrow]
        methods[situation](data)
        if situation == 1:
            self.action.reset()
            if self.image.verify()[0] == 1:
                if len(data) == 2:
                    methods[situation](data[::-1])
                elif len(data) == 4:
                    for i in range(1,4):
                        methods[situation](data, type=i)
                        self.action.reset()
                        if not self.image.verify()[0] == 1:
                            break

        return False

    def verifing(self, timeTake = 10):
        print("Verify Thread Start with timeTake = ", timeTake)
        while not self.stopSignal:
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

    def hunt(self):
        ret = self.image.checkMonster()
        if ret != None:
            self.action.click(ret,right=False)


    def dig(self):
        right_signal = False
        if self.dig_count >= 6:
            right_signal = True
        self.action.dig(right_signal)
        self.dig_count += 1
        if self.dig_count >= 12:
            self.dig_count = 0

    def checkdiv(self):
        divret = self.image.div(6)
        return divret

    def eat(self):
        self.div = self.checkdiv()
        if self.div != None:
            monster = []
            rubbish = []
            for x,y,w,h in self.div:
                middle_x = x + w // 2
                middle_y = y + h // 2
                self.lock_verify.acquire()
                self.action.move((middle_x, middle_y), 0.05)
                self.lock_verify.release()
                type_hand = self.image.checkMouse((middle_x, middle_y)) #0->food 1->monster 2->big rubbish
                if type_hand == 0:
                    self.lock_verify.acquire()
                    self.action.click((middle_x, middle_y))
                    self.lock_verify.release()
                    time.sleep(10)
                    # return
                if type_hand == 1:
                    monster.append((middle_x,middle_y))
                elif type_hand == 2:
                    rubbish.append((middle_x, middle_y))
                elif type_hand == 3:
                    self.forbinpoint.append((x,y,w,h))
            if len(monster) > 0:
                self.lock_verify.acquire()
                self.action.click(monster[0], right=True)
                self.lock_verify.release()
                return

            if len(rubbish) > 0:
                self.lock_verify.acquire()
                self.action.click(rubbish[0],right=True)
                self.lock_verify.release()
                return

    def earn(self):
        roomtype = self.image.checkBackGround() # 0->start 1->new 2->hunt 3->hometown 4->room
        print('what',roomtype)
        if roomtype == 4:
            print("There is Room and quit")
            self.lock_verify.acquire()
            self.action.click(self.action.quitLocation)
            self.lock_verify.release()
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
                self.lock_verify.acquire()
                self.action.click(location)
                self.lock_verify.release()
                time.sleep(2)
            print('Finish collecting and quit the room')
            #quit the room
            self.lock_verify.acquire()
            self.action.click(self.action.quitLocation)
            self.lock_verify.release()
            self.room_count += 1

    def noappThread(self, function, timeTake=0):
        while not self.stopSignal:
            function()
            if timeTake > 0:
                time.sleep(timeTake)

    def appThread(self, function, timeTake=0):
        while not self.stopSignal:
            self.lock_verify.acquire()
            function()
            self.lock_verify.release()
            if timeTake > 0:
                time.sleep(timeTake)

    def start(self, mode= 0):
        workmode = [
            [(self.fishflag, 30), (self.fish, 0)],
            [(self.hunt, 0.5), (self.transfer, 20)],
            [(self.dig, 4)],
            [(self.eat, 0)],
            [(self.earn, 0)]][mode]

        theThread = self.noappThread if mode == 4 or mode == 3 else self.appThread

        for work, timeTake in workmode:
            self.thread.append(th.Thread(target=theThread, args=(work, timeTake)))
            print(work.__name__, " Thread Start with timeTake = ", timeTake)

        for thread in self.thread:
            thread.start()



if __name__ == '__main__':
    print('*' * 20)
    time.sleep(2)
    program = AntYecai(test=True)
    program.mouseLocation()

    print(
        """
    Work Mode:
    0: Fish
    1: Hunting
    2: Diging
    3: Eating with hunting
    4: Earning
    5: Earn Snow with North
    """
    )
    program.start(2)





    # rubbish
    # program = AntYecai(test=True)
    # program.mouseLocation()
    # rubbishMan = (576, 283)
    # rubbishUp = (734, 376)
    # rubbishExchange = (574, 470)
    # rubbishStop = [(467, 444),(569, 449),(683, 444)]
    #
    # #click rubbish man
    # while True:
    #     program.action.click(rubbishMan)
    #     #click rubbish up
    #     for i in range(3):
    #         program.action.click(rubbishUp)
    #     #exchange
    #     program.action.click(rubbishExchange)
    #
    #     for i in range(3):
    #         program.action.click(rubbishStop[i])
    #     time.sleep(5)
