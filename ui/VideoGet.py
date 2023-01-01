from threading import Thread
import cv2
import time

class VideoGet:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src, cv2.CAP_DSHOW)
        self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        time.sleep(2.0)

        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        (self.grabbed, self.frame) = self.stream.read()

        self.w = int(self.stream.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.h = int(self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT))


        # Capture from camera
        self.zb  = 300
        self.hzb = int(self.zb / 2)
        self.cx  = int((self.w / 2) - self.hzb)
        self.cy  = int((self.h / 2) - self.hzb)

        print("WH: " + str(self.w) + ", " + str(self.h))
        print("C: " + str(self.cx) + ", " + str(self.cy))

        self.zoomw = 1920 - self.w
        self.zoomh = self.h

        self.stopped = False

    def start(self):    
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def getDim(self):
        return (self.w, self.h)

    def stop(self):
        self.stopped = True