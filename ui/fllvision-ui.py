from tkinter import *
from PIL import ImageTk, Image
import cv2
from utils import ARUCO_DICT
import numpy as np

from CountdownTimer import CountdownTimer
from VideoGet import VideoGet
from UI import UI
from RobotTracker import RobotTracker

def crop_to_robot(frame, video_getter):
    #print("Crop: " + str(video_getter.cx) + ", " + str(video_getter.cy) + ", " + str(video_getter.hzb))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.aruco_dict = cv2.aruco.Dictionary_get(aruco_dict_type)
    parameters = cv2.aruco.DetectorParameters_create()

    corners, ids, rejected_img_points = cv2.aruco.detectMarkers(gray, cv2.aruco_dict,parameters=parameters)
    
    # If markers are detected
    if len(corners) > 0:
        # Estimate pose of each marker and return the values rvec and tvec---(different from those of camera coefficients)
        #rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[0], 0.02, matrix_coefficients, distortion_coefficients)
        # Draw a square around the markers
        #cv2.aruco.drawDetectedMarkers(frame, corners) 
        
        bbox = corners[0]
        centerW = float(bbox[0][2][0] - bbox[0][0][0]) / float(2) + float(bbox[0][0][0])
        centerH = float(bbox[0][2][1] - bbox[0][0][1]) / float(2) + float(bbox[0][0][1])
        robot_tracker.center = [int(centerW), int(centerH)]

    cv2.circle(frame, robot_tracker.center, radius=5, color=(0, 255, 255), thickness=-1)
    cropped_frame = robot_tracker.crop(frame)
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


source = 1
countdown_time = 150

aruco_dict_type = ARUCO_DICT["DICT_5X5_100"]
calibration_matrix_path = "data/calibration_matrix.npy"
distortion_coefficients_path = "data/distortion_coefficients.npy"

matrix_coefficients     = np.load(calibration_matrix_path)
distortion_coefficients = np.load(distortion_coefficients_path)

robot_tracker = RobotTracker()

webcam = VideoGet(source).start()

ui = UI()
ui.root.protocol("WM_DELETE_WINDOW", onClose)
ui.init(webcam)

countdown_timer = CountdownTimer(ui, countdown_time).start()
show_frame(webcam)

ui.root.mainloop()