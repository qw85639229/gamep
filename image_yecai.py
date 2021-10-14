# -*-encoding:utf-8-*-
import pyautogui
import numpy as np
import cv2
import aircv
import collections
import pytesseract
from cnocr import CnOcr
from skimage import measure
import imutils
from imutils import contours
import sys
import os


def readimg(path):
    # path = os.path.join(os.path.dirname(os.path.realpath(sys.executable)), path)
    # assert 0, path
    # print(path)
    return cv2.imread(r'{}'.format(path))

class Image_yecai(object):
    def __init__(self, windowLeftUp):
        self.tessdata_dir_config = '--tessdata-dir "c://Program Files (x86)//Tesseract-OCR//tessdata"'
        self.ocr = CnOcr()
        self.ocr_num = CnOcr(cand_alphabet=[str(x)for x in range(10)] + ['+', '=', '?', '/'])
        """Location"""
        self.windowLeftUp = windowLeftUp
        self.verifyLeftUp = (490, 237)
        self.verifyRightDown = (806, 543)
        self.basketballLocation = (514,310,770-512,493-310)
        self.mathLocation = (534, 362, 750 - 534, 391 - 362)
        self.hanLocation = (582, 352, 694 - 582, 384 - 352)
        self.fishLocation = (706 , 310, 14, 75)
        self.fishFlagLocation = (232, 146, 309-232, 174-146)
        self.backgroundLocation = (0,0,1280,750)
        #HP
        self.hpLocation = (748, 722, 876 - 748, 724 - 722)
        self.hpThreshold = 20
        #hunting
        self.pre_location = None

        """Query Image"""
        #verify
        self.verification_img = readimg('img/verify/verification.png')
        self.basketball_img = readimg('img/verify/basketball.png')
        self.rim_img = readimg('img/verify/rim.png')
        self.enter_img = readimg('img/verify/enter.png')
        self.blank_img = readimg('img/verify/blank.png')
        self.blank_han_img = readimg('img/verify/blank_han.png')
        self.right_arrow_img = readimg('img/verify/rightarrow.png')
        self.situation4_black_img = readimg('img/verify/situation4_black.png')
        #hand
        self.food_hand_img = readimg('img/hand/food_hand.png')
        self.monster_hand_img = readimg('img/hand/monster_hand.png')
        self.rubbish_hand_img = readimg('img/hand/rubbish_hand.png')
        self.forbin_hand_img = readimg('img/hand/forbin_hand_black.png')
        #fish
        self.fishflag_img = readimg('img/fish/fishflag1.png')
        #area
        self.area_start_img = readimg('img/area/area_start.png')
        self.area_new_img = readimg('img/area/area_new.png')
        self.area_hunt_img = readimg('img/area/area_hunt.png')
        self.area_hometown_img = readimg('img/area/area_hometown.png')
        self.area_room_img = readimg('img/area/area_room.png')
        self.area_circle_img = readimg('img/area/circle.png')
        self.area_caomei_img = readimg('img/area/caomei.png')
        self.area_notice = readimg('img/area/notice.png')
        self.area_enter = readimg('img/area/enter.png')
        self.area_snow2 = readimg('img/area/snow2.png')
        self.area_snow3 = readimg('img/area/snow3.png')
        self.area_snow4 = readimg('img/area/snow4.png')
        self.area_snow5 = readimg('img/area/snow5.png')
        #food
        self.food_caomei_img = readimg('img/food/food_caomei.png')
        self.food_lizi_img = readimg('img/food/food_lizi.png')
        self.food_lushui_img = readimg('img/food/food_lushui.png')
        #rubbish
        self.rubbish_apple_img = readimg('img/rubbish/apple.png')
        self.rubbish_guo_img = readimg('img/rubbish/guo.png')
        self.rubbish_hat_img = readimg('img/rubbish/hat.png')
        self.rubbish_nongyao_img = readimg('img/rubbish/nongyao.png')
        self.rubbish_paomo_img = readimg('img/rubbish/paomo.png')
        self.rubbish_shoe_img = readimg('img/rubbish/shoe.png')
        self.rubbish_wan_img = readimg('img/rubbish/wan.png')
        self.rubbish_zhi_img = readimg('img/rubbish/zhi.png')
        self.rubbish_caffe_img = readimg('img/rubbish/caffe.png')
        self.rubbish_gold_img = readimg('img/rubbish/gold.png')
        self.rubbish_hat2_img = readimg('img/rubbish/hat2.png')
        self.rubbish_iron_img = readimg('img/rubbish/iron.png')
        self.rubbish_pot_img = readimg('img/rubbish/pot.png')
        self.rubbish_tyre_img = readimg('img/rubbish/tyre.png')
        self.rubbish_paomian_img = readimg('img/rubbish/paomian.png')
        self.rubbish_pan_img = readimg('img/rubbish/pan.png')

        self.background_imgs = []

    def reLo(self, location):
        return (location[0] + self.windowLeftUp[0], location[1] + self.windowLeftUp[1])

    def mouseLocation(self):
        (x,y) = pyautogui.position()
        print(f"Absolute coordinates: ({x} , {y})" )
        print(f"Relative coordinates: ({x - self.windowLeftUp[0]} , {y - self.windowLeftUp[1]})" )

    def shoot(self, x, y, w, h, absolute=False, show=False):
        if not absolute:
            x,y = self.reLo((x,y))
            # w,h = self.reLo((w,h))
        img = np.array(pyautogui.screenshot(region=(x,y,w,h,)))[:,:,[2,1,0]]
        if show:
            cv2.imshow('t',img)
            cv2.waitKey()
        return img

    def verify(self):
        img = self.shoot(*self.verifyLeftUp, self.verifyRightDown[0] - self.verifyLeftUp[0], self.verifyRightDown[1] - self.verifyLeftUp[1])
        ret = aircv.find_all_template(img, self.verification_img, threshold=0.7)
        if len(ret) <= 0:
            return 0, None

        """1: basketball"""
        ret = aircv.find_all_template(img, self.basketball_img, threshold=0.7)
        if len(ret) > 0:
            return 1, self.basketball()

        """2: Enter A Word Math"""
        ret = aircv.find_all_template(img, self.enter_img)
        ret2 = aircv.find_all_template(img, self.blank_img)
        if len(ret) > 0 and len(ret2) > 0:
            (max_math_num, enterLocation, blankLocation) = self.wordMath(ret[0]['result'], ret2[0]['result'])
            if max_math_num == -1:
                return 0, None
            return 2, (max_math_num, enterLocation, blankLocation)

        """3: Enter A Word Sim Han"""
        ret2 = aircv.find_all_template(img, self.blank_han_img)
        if len(ret) > 0 and len(ret2) > 0:
            (max_han_word, enterLocation, blankLocation) = self.wordHan(ret[0]['result'], ret2[0]['result'])
            if max_han_word == -1:
                return 0, None
            return 3, (max_han_word, enterLocation, blankLocation)

        """4: Right Arrow"""
        ret = aircv.find_all_template(img, self.right_arrow_img)
        if len(ret) > 0:
            return 4, self.rightArrow(img, ret[0]['result'], True)

        return 0, None

    def iou(self, box1, box2):
        '''
        box:[x1, y1, x2, y2]
        '''
        box1 = (box1[0], box1[1], box1[0] + box1[2], box1[1] + box1[3])
        box2 = (box2[0], box2[1], box2[0] + box2[2], box2[1] + box2[3])

        in_h = min(box1[3], box2[3]) - max(box1[1], box2[1])
        in_w = min(box1[2], box2[2]) - max(box1[0], box2[0])
        inner = 0 if in_h < 0 or in_w < 0 else in_h * in_w
        union = (box1[2] - box1[0]) * (box1[3] - box1[1]) + \
                (box2[2] - box2[0]) * (box2[3] - box2[1]) - inner
        # print(inner)
        iou = inner / union
        return iou

    def basketball(self):
        background = self.shoot(*self.basketballLocation)
        img = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
        binary = cv2.bitwise_not(binary)
        # cv2.imshow('r',binary)
        # cv2.waitKey()
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        ret = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w * h <= 400 or w * h >= 60 * 60:
                continue
            # cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            ret.append((x, y, w, h))
        # cv2.imshow('r',img)
        # cv2.waitKey()
        ret.sort(key=lambda x: x[2] * x[3], reverse=True)
        ans = []
        iou_threshold = 0.2
        for i in ret:
            ans.append(i)
            for j in range(len(ans) - 1):
                iou_value = self.iou(i, ans[j])
                # print(iou_value)
                if iou_value >= 0.2:
                    ans.pop()
                    break
        location1 = self.reLo((100,100))
        location2 = self.reLo((100,100))
        if len(ans) == 2:
            location1 = self.reLo((ans[0][0] + ans[0][2] // 2 + self.basketballLocation[0], ans[0][1] + ans[0][3] // 2 + self.basketballLocation[1]))
            location2 = self.reLo((ans[1][0] + ans[1][2] // 2 + 10 + self.basketballLocation[0], ans[1][1] + ans[1][3] // 2 + self.basketballLocation[1]))
        elif len(ans) == 1:
            # length = ans[0][2]
            # location1 = self.reLo((ans[0][0] + 10 + self.basketballLocation[0], ans[0][1] + ans[0][3] // 2 + self.basketballLocation[1]))
            # location2 = self.reLo((ans[0][0] + length + self.basketballLocation[0], ans[0][1] + ans[0][3] // 2 + self.basketballLocation[1]))
            x,y,w,h = ans[0]
            x,y = self.reLo((x+self.basketballLocation[0],y+self.basketballLocation[1]))
            return [x,y,w,h]
        return [location1, location2]


    def wordMath(self, enterLocation, blankLocation):
        enterLocation = tuple([int(x) for x in enterLocation])
        blankLocation = tuple([int(x) for x in blankLocation])
        enterLocation = self.reLo((enterLocation[0] + self.verifyLeftUp[0], enterLocation[1] + self.verifyLeftUp[1]))
        blankLocation = self.reLo((blankLocation[0] + self.verifyLeftUp[0], blankLocation[1] + self.verifyLeftUp[1]))

        math_count = 0
        math_dict = collections.defaultdict(int)
        max_math_count = 0
        max_math_num = -1

        for i in range(30):
            math_img = self.shoot(*self.mathLocation)
            # math_string = pytesseract.image_to_string(math_img, config=self.tessdata_dir_config, lang='chi_sim')
            math_string = self.ocr_num.ocr(math_img)
            # print(math_string)
            if len(math_string) <= 0:
                continue
            math_string = ''.join(math_string[0][0])
            # print(math_string)
            # exit()
            # math_string = ''.join(math_string[0])
            # print(math_string)
            # math_string = None
            math_string.rstrip()
            if '=' in math_string or '?' in math_string:
                math_string = math_string.split('\n')[0][:-2]
                # print(math_string)
                for i in ['+', '-', 'x', '%']:
                    if i in math_string:
                        maths_num = math_string.split(i)
                        if len(maths_num) != 2 or not maths_num[0].isdigit() or not maths_num[1].isdigit():
                            break
                        math_count += 1
                        a = int(maths_num[0])
                        b = int(maths_num[1])
                        if i == 'x':
                            target_num = a * b

                        elif i == '+':
                            target_num = a + b
                        elif i == '-':
                            target_num = a - b
                        else:
                            target_num = a // b
                        math_dict[target_num] += 1
                        if math_dict[target_num] > max_math_count:
                            max_math_count = math_dict[target_num]
                            max_math_num = target_num
        # print(math_dict)
        # print('max_math_num: ', max_math_num)
        # exit()
        return (max_math_num, enterLocation, blankLocation)

    def wordHan(self, enterLocation, blankLocation):
        enterLocation = tuple([int(x) for x in enterLocation])
        blankLocation = tuple([int(x) for x in blankLocation])
        enterLocation = self.reLo(
            (enterLocation[0] + self.verifyLeftUp[0], enterLocation[1] + self.verifyLeftUp[1]))
        blankLocation = self.reLo(
            (blankLocation[0] + self.verifyLeftUp[0], blankLocation[1] + self.verifyLeftUp[1]))

        han_dict = collections.defaultdict(int)
        max_han_count = 0
        max_han_word = -1
        for i in range(30):
            han_img = self.shoot(*self.hanLocation)
            han_img = cv2.resize(han_img,(han_img.shape[1]*3,han_img.shape[0]*3))
            try:
                han_word, prob = self.ocr.ocr(han_img)[0]
                # han_word, prob = None, None
                # print(han_word)
                for j in han_word:
                    if '\u4e00' <= j <= '\u9fff':
                        han_dict[j] += 1
                        if han_dict[j] > max_han_count:
                            max_han_count = han_dict[j]
                            max_han_word = j
            except:
                pass
        return (max_han_word, enterLocation, blankLocation)

    def rightArrow(self, img=None, rightArrowLocation=(0,0), detect=True):

        if detect:
            rightArrowLocation = tuple([int(x) for x in rightArrowLocation])
            rightArrowLocation = self.reLo(
                (rightArrowLocation[0] + self.verifyLeftUp[0], rightArrowLocation[1] + self.verifyLeftUp[1]))
            self.preRightArrow = img
            self.rightArrowLocation = rightArrowLocation
            return (rightArrowLocation)
        else:
            next_img = self.shoot(*self.verifyLeftUp, self.verifyRightDown[0] - self.verifyLeftUp[0],
                             self.verifyRightDown[1] - self.verifyLeftUp[1])
            div = next_img - self.preRightArrow
            div = np.abs(div)
            div = np.array(div, np.uint8)
            div = cv2.cvtColor(div, cv2.COLOR_BGR2GRAY)
            ret, div = cv2.threshold(div, 0, 255, type=cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(div, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            ret = None
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                if not 40 * 40 <= w * h <= 70 * 70 or not abs(w - h) <= 5:
                    continue
                else:
                    ret = (x, y, w, h)
                    break

            if ret == None:
                return (80 + self.verifyLeftUp[0] + self.windowLeftUp[0], rightArrowLocation[1])

            strip_img = self.preRightArrow[ret[1]:ret[1]+ret[3], :, :]
            strip_img = cv2.cvtColor(strip_img, cv2.COLOR_BGR2GRAY)
            strip_img = np.array(strip_img,dtype=np.float)
            strip_value = np.mean(strip_img, axis=0)
            for i in range(30, strip_img.shape[0] - 30):
                strip_value[i] = sum(strip_value[i-20:i+20]) / 40
            index = np.argmin(strip_value)
            return (index + self.verifyLeftUp[0] + self.windowLeftUp[0], rightArrowLocation[1])


        #
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 1)
        # contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # ret = (80, 0, 0, 0)
        # for contour in contours:
        #     x, y, w, h = cv2.boundingRect(contour)
        #     if not 40 * 40 <= w * h <= 70 * 70 or not abs(w - h) <= 5:
        #         continue
        #     if x > ret[0]:
        #         ret = (x, y, w, h)
                # cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 4)
        # # cv2.imshow('r',img)
        # # cv2.waitKey()
        # # exit()
        # return (rightArrowLocation, (ret[0] + ret[2] // 2 + self.verifyLeftUp[0] + self.windowLeftUp[0], rightArrowLocation[1]))

    def fish(self):
        img = self.shoot(*self.fishLocation)
        # cv2.imshow('r',img)
        # cv2.waitKey()
        # exit()
        fish_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        fish_strip = fish_img[:, fish_img.shape[1] // 2]
        min_fish_strip_index = np.argmin(fish_strip)
        return min_fish_strip_index / (fish_img.shape[0] // 2)

    def fishflag(self):
        img = self.shoot(*self.fishFlagLocation)
        # cv2.imshow('r',img)
        # cv2.waitKey()
        # ret = aircv.find_all_template(img, self.fishflag_img)
        # if len(ret) > 0:
        #     return False
        ret = self.ocr.ocr(img)
        for i in ret[0][0]:
            if i in '停止垂钓':
                # print("保持钓鱼状态")
                return False
        return True

    def checkMonster(self):
        img = self.shoot(*self.backgroundLocation)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        ret = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if not (60 <= w <= 80 and 5 <= h <= 10):
                continue
            ret.append((x + w // 2, max(1, y - 80)))

        if self.pre_location == None:
            if len(ret) > 0:
                return ret[0]
            return None

        next_location = None
        min_distance_2 = 1280 * 1280
        for x,y in ret:
            cur_distance_2 = (x - self.pre_location[0])**2 + (y - self.pre_location[1])**2
            if cur_distance_2 <= min_distance_2:
                min_distance_2 = cur_distance_2
                next_location = (x,y)

        self.pre_location = next_location
        return next_location

    def checkHP(self):
        img = self.shoot(*self.hpLocation)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = np.mean(img, axis=0)
        length = img.shape[0]
        for i in range(length):
            if img[i] <= self.hpThreshold:
                return i/length
        return 1


    def smearDetect(self, img, areaThreshold=4000):
        # img = ~img
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # blurred = cv2.GaussianBlur(gray, (11, 11), 0)
        # thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]
        thresh = img
        thresh1 = cv2.erode(thresh, None, iterations=2)
        thresh2 = cv2.dilate(thresh1, None, iterations=4)
        labels = measure.label(thresh2, connectivity=2, background=0)
        mask = np.zeros(thresh.shape, dtype="uint8")
        for label in np.unique(labels):
            if label == 0:
                continue
            labelMask = np.zeros(thresh.shape, dtype="uint8")
            labelMask[labels == label] = 255
            numPixels = cv2.countNonZero(labelMask)
            if numPixels > areaThreshold:
                mask = cv2.add(mask, labelMask)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        if len(cnts) == 0:
            return None
        cnts = contours.sort_contours(cnts)[0]
        ret = []
        for (i, c) in enumerate(cnts):
            # draw the bright spot on the image
            (x, y, w, h) = cv2.boundingRect(c)
            ret.append((x, y, w, h))
        return ret

    def div(self, num):
        img = self.shoot(*self.backgroundLocation)
        if len(self.background_imgs) < num:
            self.background_imgs.append(img)
            return None
        self.background_imgs.append(img)
        background = self.background_imgs.pop(0)
        background = np.array(background, dtype=np.int8)
        img = np.array(img, dtype=np.int8)
        div = img - background
        div = np.abs(div)
        div = np.array(div, np.uint8)
        div = cv2.cvtColor(div, cv2.COLOR_BGR2GRAY)
        ret, div = cv2.threshold(div, 0, 255, type=cv2.THRESH_BINARY)
        kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (4,4))
        div = cv2.erode(div, kernel1)
        ret = self.smearDetect(div, 100)
        return ret

    def checkMouse(self, location):
        img = self.shoot(location[0]-5, location[1]-5, 30, 30 )
        ret = aircv.find_all_template(img, self.food_hand_img, threshold=0.6)
        if len(ret) > 0:
            return 0
        ret = aircv.find_all_template(img, self.monster_hand_img, threshold=0.6)
        if len(ret) > 0:
            return 1
        ret = aircv.find_all_template(img, self.rubbish_hand_img, threshold=0.6)
        if len(ret) > 0:
            return 2
        ret = aircv.find_all_template(img, self.forbin_hand_img, threshold=0.6)
        if len(ret) > 0:
            return 3
        return -1

    def checkBackGround(self, checksnow=False):
        background_img = [self.area_start_img,
                          self.area_new_img,
                          self.area_hunt_img,
                          self.area_hometown_img,
                          self.area_room_img,
                          self.area_snow2,
                          self.area_snow3,
                          self.area_snow4,
                          self.area_snow5
                          ]

        img = self.shoot(*self.backgroundLocation)
        # cv2.imshow('r',img)
        # cv2.waitKey()
        # exit()
        startPoint = 5 if checksnow else 0
        for i in range(startPoint, len(background_img)):
            ret = aircv.find_all_template(img, background_img[i], threshold=0.9)
            if len(ret) > 0:
                return i
        return -1

    def checkRoomCircle(self):
        img = self.shoot(*self.backgroundLocation)
        ret = aircv.find_all_template(img, self.area_circle_img, threshold=0.8)
        ans = []
        for i in ret:
            ans.append(tuple(map(int, i['result'])))
        ans.sort(key = lambda x:x[1])
        return ans

    def checkRoomCaomei(self):
        img = self.shoot(*self.backgroundLocation)
        ret = aircv.find_all_template(img, self.area_caomei_img, threshold=0.8)
        ans = []
        for i in ret:
            ans.append(tuple(map(int, i['result'])))
        ans.sort(key = lambda x:x[1])
        return ans

    def checkFoodRubbish(self, food=True, rubbish=True):
        food_img = [self.food_caomei_img,
                    self.food_lizi_img,
                    self.food_lushui_img]
        rubbish_img = [self.rubbish_apple_img,
                       self.rubbish_guo_img,
                       self.rubbish_hat_img,
                       self.rubbish_nongyao_img,
                       self.rubbish_paomo_img,
                       self.rubbish_shoe_img,
                       self.rubbish_wan_img,
                       self.rubbish_zhi_img,
                       self.rubbish_caffe_img,
                       self.rubbish_gold_img,
                       self.rubbish_hat2_img,
                       self.rubbish_iron_img,
                       self.rubbish_pot_img,
                       self.rubbish_tyre_img,
                       self.rubbish_paomian_img,
                       self.rubbish_pan_img
                       ]
        ret = []
        background = self.shoot(*self.backgroundLocation)
        if food:
            for img in food_img:
                target = aircv.find_all_template(background, img, threshold=0.7)
                if len(target) > 0:
                    ret.append(tuple(map(int, target[0]['result'])))
        if rubbish:
            for img in rubbish_img:
                target = aircv.find_all_template(background, img, threshold=0.7)
                if len(target) > 0:
                    ret.append(tuple(map(int, target[0]['result'])))
        return ret

    def checkNotice(self):
        img = self.shoot(*self.backgroundLocation)
        ret = aircv.find_all_template(img, self.area_notice, threshold=0.9)
        # assert 0, ret
        if len(ret) > 0:
            ret = aircv.find_all_template(img, self.area_enter, threshold=0.9)
            if len(ret) > 0:
                return tuple(map(int, ret[0]['result']))
        return None

if __name__ == "__main__":
    img = cv2.imread('img/test/test8.png')

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mean_value = np.mean(gray)
    # ret, binary = cv2.threshold(gray, mean_value, 255, cv2.THRESH_TOZERO_INV)
    # gray = cv2.bitwise_not(gray)
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # binary = cv2.bitwise_not(binary)
    cv2.imshow('r',binary)
    cv2.waitKey()
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    ret = (80, 0, 0, 0)
    # print(ret[0])
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if not 40 * 40 <= w * h <= 70 * 70 or not abs(w - h) <= 5:
            continue
        # print(x,y,w,h)
        if x > ret[0]:
            ret = (x, y, w, h)
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 4)
    cv2.imshow('r',img)
    cv2.waitKey()
