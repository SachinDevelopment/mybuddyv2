import time
import pyautogui
import random
import keyboard
import cv2 as cv
pyautogui.FAILSAFE = True ## This enables you to cancel 

stop = False
def onkeypress(event):
    global stop
    if event.name == 'esc':
        stop = True

# ---------> hook event handler
keyboard.on_press(onkeypress)

def test():
    while 1==1:
        if not stop:
            trees = ['willow1.png', 'willow2.png', 'willow3.png', 'willow4.png', 'willow5.png', 'willow6.png', 'willow7.png', 'willow8.png' ]
            fullinv = pyautogui.locateOnScreen('fullinv.png', confidence=.95)
            if(fullinv):
                for log in pyautogui.locateAllOnScreen('log.png', confidence=0.8):
                    center = pyautogui.center(log)
                    pyautogui.moveTo(center, duration=0)
                    pyautogui.click()
            for tree in trees:
                found = pyautogui.locateOnScreen(tree, confidence=.4)
                if(found and pyautogui.locateOnScreen('woodcutting.png', confidence=.5) == None):
                    print('tree found', tree, 'loc', found)
                    centeroftree = pyautogui.center(found)
                    pyautogui.moveTo(centeroftree, duration=random.randint(1, 2))
                    pyautogui.click()
                    time.sleep(3)
        else:
            break
test()