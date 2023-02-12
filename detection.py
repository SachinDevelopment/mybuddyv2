import cv2 as cv
from threading import Thread, Lock
from hsvfilter import HsvFilter

class Detection:

    # threading properties
    stopped = True
    lock = None
    rectangles = []
    # properties
    screenshot = None
    vision_tree = None
    processed_img = None
    hsv_filter = HsvFilter(110, 178, 53, 135, 226, 255, 0, 32, 120, 165)

    def __init__(self, vision_tree):
        # create a thread lock object
        self.lock = Lock()
        self.vision_tree = vision_tree

    def update(self, screenshot):
        self.lock.acquire()
        self.processed_img = self.vision_tree.apply_hsv_filter(screenshot, self.hsv_filter)
        self.screenshot = screenshot
        self.lock.release()

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        # TODO: you can write your own time/iterations calculation to determine how fast this is
        while not self.stopped:
            if not self.screenshot is None:
                # do object detection
                rectangles = self.vision_tree.find(self.processed_img, .4)

                # lock the thread while updating the results
                self.lock.acquire()
                self.rectangles = rectangles
                self.lock.release()
