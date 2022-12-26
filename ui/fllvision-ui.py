from tkinter import *
from PIL import ImageTk, Image
import cv2
import time

from CountdownTimer import CountdownTimer
from VideoGet import VideoGet
from UI import UI

source = 1
countdown_time = 150

def crop_to_robot(frame, video_getter):
    #print("Crop: " + str(video_getter.cx) + ", " + str(video_getter.cy) + ", " + str(video_getter.hzb))
    cropped_frame = frame[video_getter.cy:video_getter.cy+video_getter.hzb, video_getter.cx:video_getter.cx+video_getter.hzb]
    return cropped_frame

def show_frame(video_getter):

    cv2image = video_getter.frame    
    cropped = crop_to_robot(cv2image, video_getter)
    ui.display(cv2image, cropped)
    
    ui.root.after(20, show_frame, video_getter)


def onClose():
    print("stopping threads")
    webcam.stop()
    countdown_timer.stop()
    ui.root.destroy()

webcam = VideoGet(source).start()

ui = UI()
ui.root.protocol("WM_DELETE_WINDOW", onClose)
ui.init(webcam)

countdown_timer = CountdownTimer(ui, countdown_time).start()
show_frame(webcam)

ui.root.mainloop()