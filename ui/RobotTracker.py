from threading import Thread
import cv2
import time

class RobotTracker:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self):
        self.center = [300, 300]
        self.padding = 100

    def get_center(self):
        return self.center

    def crop(self, frame):
        ya = max(0, self.center[1] - self.padding)
        yb = max(0, self.center[1] + self.padding)
        xa = max(0, self.center[0] - self.padding)
        xb = max(0, self.center[0] + self.padding)
        return frame[ya : yb, xa : xb]