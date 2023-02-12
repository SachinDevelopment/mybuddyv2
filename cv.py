import cv2 as cv
import numpy as np
import os
from time import time, sleep
from windowcapture import WindowCapture
from vision import Vision
import pyautogui
import random
from threading import Thread
from bot import AustinmBot, BotState
from detection import Detection


os.chdir(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

wincap = WindowCapture('RuneLite - CuredAustinm')
vision = Vision("needle_processed.jpg")
detector = Detection(vision_tree=vision)
bot = AustinmBot((wincap.offset_x, wincap.offset_y), (wincap.w, wincap.h))
wincap.start()
detector.start()
bot.start()
loop_time = time()
while(True):

    # if we don't have a screenshot yet, don't run the code below this point yet
    if wincap.screenshot is None:
        continue

    # give detector the current screenshot to search for objects in
    detector.update(wincap.screenshot)

    # update the bot with the data it needs right now
    if bot.state == BotState.INITIALIZING:
        # while bot is waiting to start, go ahead and start giving it some targets to work
        # on right away when it does start
        targets = vision.get_click_points(detector.rectangles)
        bot.update_targets(targets)
    elif bot.state == BotState.SEARCHING:
        # when searching for something to click on next, the bot needs to know what the click
        # points are for the current detection results. it also needs an updated screenshot
        # to verify the hover tooltip once it has moved the mouse to that position
        targets = vision.get_click_points(detector.rectangles)
        bot.update_targets(targets)
        bot.update_screenshot(wincap.screenshot)

    if DEBUG:
        # draw the detection results onto the original image
        detection_image = vision.draw_rectangles( wincap.screenshot, detector.rectangles)
        # display the images
        cv.imshow('Tismoclient', detection_image)
        # debug the loop rate
        # print('FPS {}'.format(1 / (time() - loop_time)))
        loop_time = time()
    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    key = cv.waitKey(1)
    if key == ord('q'):
        wincap.stop()
        detector.stop()
        bot.stop()
        cv.destroyAllWindows()
        break

print('Done.')

