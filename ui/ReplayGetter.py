from threading import Thread
import cv2
import time

class ReplayGetter:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self, fileFullRes='output-wide.mp4', fileCropped='output-zoom.mp4'):
        self.fileFullRes = fileFullRes
        self.fileCropped = fileCropped
        self.fullres_frame_counter = 0
        self.cropped_frame_counter = 0
    
    def open(self):
        print("opening replay")
        self.capFullRes = cv2.VideoCapture(self.fileFullRes)
        self.capCropped = cv2.VideoCapture(self.fileCropped)
        print('fullres frame count', str(self.capFullRes.get(cv2.CAP_PROP_FRAME_COUNT)))
        print('cropped frame count', str(self.capCropped.get(cv2.CAP_PROP_FRAME_COUNT)))
        if (self.capFullRes.isOpened() == False): 
            print("Error opening video stream or file")

    def getNextFullResFrame(self):
        ret, frame = self.capFullRes.read()
        self.fullres_frame_counter += 1
        if self.fullres_frame_counter == self.capFullRes.get(cv2.CAP_PROP_FRAME_COUNT):
            print('reset full res to start')
            self.fullres_frame_counter = 0
            self.capFullRes.set(cv2.CAP_PROP_POS_FRAMES, 0)
        return frame

    def getNextCroppedFrame(self):
        ret, frame = self.capCropped.read()
        self.cropped_frame_counter += 1
        if self.cropped_frame_counter == self.capCropped.get(cv2.CAP_PROP_FRAME_COUNT):
            print('reset full res to start')
            self.cropped_frame_counter = 0
            self.capCropped.set(cv2.CAP_PROP_POS_FRAMES, 0)
        return frame

    def close(self):
        self.capFullRes.release()
        self.capCropped.release()
        self.frame_counter = 0
