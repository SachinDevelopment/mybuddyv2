import cv2 as cv
import pyautogui
from time import sleep, time
from threading import Thread, Lock
from math import sqrt


class BotState:
    INITIALIZING = 0
    SEARCHING = 1
    MOVING = 2
    MINING = 3
    BACKTRACKING = 4


class AustinmBot:
    
    # constants
    INITIALIZING_SECONDS = 6

    # threading properties
    stopped = True
    lock = None

    # properties
    state = None
    targets = []
    screenshot = None
    timestamp = None
    window_offset = (0,0)
    window_w = 0
    window_h = 0
    woodcutting_tooltip = None
    click_history = []

    def __init__(self, window_offset, window_size):
        # create a thread lock object
        self.lock = Lock()

        # for translating window positions into screen positions, it's easier to just
        # get the offsets and window size from WindowCapture rather than passing in 
        # the whole object
        self.window_offset = window_offset
        self.window_w = window_size[0]
        self.window_h = window_size[1]

        # pre-load the needle image used to confirm our object detection
        self.woodcutting_tooltip = cv.imread('woodcutting.png', cv.IMREAD_UNCHANGED)

        # start bot in the initializing mode to allow us time to get setup.
        # mark the time at which this started so we know when to complete it
        self.state = BotState.INITIALIZING
        self.timestamp = time()

    def click_next_target(self):
        targets = self.targets_ordered_by_distance(self.targets)
        fullinv = pyautogui.locateOnScreen('fullinv.png', confidence=.8)
        if(fullinv):
            for log in pyautogui.locateAllOnScreen('log.png', confidence=0.8):
                center = pyautogui.center(log)
                pyautogui.moveTo(center, duration=0)
                pyautogui.click()
        else:
            if len(targets) > 0 and pyautogui.locateOnScreen('woodcutting.png', confidence=.5) == None:
                target_pos = targets[0]
                screen_x, screen_y = self.get_screen_position(target_pos)
                pyautogui.moveTo(x=screen_x, y=screen_y)
                pyautogui.click()
                sleep(2)


    def targets_ordered_by_distance(self, targets):
        # our character is always in the center of the screen
        my_pos = (self.window_w / 2, self.window_h / 2)
        # searched "python order points by distance from point"
        # simply uses the pythagorean theorem
        # https://stackoverflow.com/a/30636138/4655368
        def pythagorean_distance(pos):
            return sqrt((pos[0] - my_pos[0])**2 + (pos[1] - my_pos[1])**2)
        targets.sort(key=pythagorean_distance)

        return targets

    # translate a pixel position on a screenshot image to a pixel position on the screen.
    # pos = (x, y)
    # WARNING: if you move the window being captured after execution is started, this will
    # return incorrect coordinates, because the window position is only calculated in
    # the WindowCapture __init__ constructor.
    def get_screen_position(self, pos):
        return (pos[0] + self.window_offset[0], pos[1] + self.window_offset[1])

    # threading methods

    def update_targets(self, targets):
        self.lock.acquire()
        self.targets = targets
        self.lock.release()

    def update_screenshot(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    # main logic controller
    def run(self):
        while not self.stopped:
            if self.state == BotState.INITIALIZING:
                # do no bot actions until the startup waiting period is complete
                if time() > self.timestamp + self.INITIALIZING_SECONDS:
                    # start searching when the waiting period is over
                    self.lock.acquire()
                    self.state = BotState.SEARCHING
                    self.lock.release()

            elif self.state == BotState.SEARCHING:
                # check the given click point targets, confirm a limestone deposit,
                # then click it.
                success = self.click_next_target()
                # if not successful, try one more time
                if not success:
                    success = self.click_next_target()