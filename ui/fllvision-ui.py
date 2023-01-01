from tkinter import *
from PIL import ImageTk, Image
import cv2
from RecordingManager import RecordingManager
from utils import ARUCO_DICT
import numpy as np

from CountdownTimer import CountdownTimer
from VideoGet import VideoGet
from UI import UI
from RobotTracker import RobotTracker



def onClose():
    print("stopping threads")
    webcam.stop()
    countdown_timer.stop()
    ui.root.destroy()


source = 0
countdown_time = 150

aruco_dict_type = ARUCO_DICT["DICT_5X5_100"]
calibration_matrix_path = "data/calibration_matrix.npy"
distortion_coefficients_path = "data/distortion_coefficients.npy"

matrix_coefficients     = np.load(calibration_matrix_path)
distortion_coefficients = np.load(distortion_coefficients_path)

robot_tracker = RobotTracker()
rec_mgr = RecordingManager()

webcam = VideoGet(source).start()

ui = UI()
ui.root.protocol("WM_DELETE_WINDOW", onClose)

countdown_timer = CountdownTimer(ui, countdown_time)
ui.init(webcam, countdown_timer, rec_mgr, robot_tracker)
ui.show_frame(webcam)

ui.root.mainloop()