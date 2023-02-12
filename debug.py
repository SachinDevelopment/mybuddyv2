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
vision.init_control_gui()
loop_time = time()
while(True):

    # get an updated image of the game
    screenshot = wincap.get_screenshot()

    # pre-process the image
    processed_image = vision.apply_hsv_filter(screenshot)

    # do object detection
    rectangles = vision.find(processed_image, 0.46)

    # draw the detection results onto the original image
    output_image = vision.draw_rectangles(screenshot, rectangles)

    # display the processed image
    cv.imshow('Processed', processed_image)
    # cv.imshow('Matches', output_image)

    # debug the loop rate
    # print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')
