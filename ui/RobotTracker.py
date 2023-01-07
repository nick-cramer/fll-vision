from threading import Thread
import cv2
import numpy as np

class RobotTracker:
    """
    Class that RobotTracker.
    """

    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    parameters = cv2.aruco.DetectorParameters()
    parameters.minMarkerPerimeterRate = 0.01
    parameters.maxMarkerPerimeterRate = 0.1

    def __init__(self):
        self.center = [300, 300]
        self.padding = 200

    def get_center(self):
        return self.center

    def crop(self, frame):
        ya = max(0, self.center[1] - self.padding)
        yb = max(0, self.center[1] + self.padding)
        xa = max(0, self.center[0] - self.padding)
        xb = max(0, self.center[0] + self.padding)
        return frame[ya : yb, xa : xb]
        #frame = np.zeros((400, 400, 3), dtype='uint8')
        #return frame

    def crop_to_robot(self, frame, video_getter):
        #print("Crop: " + str(video_getter.cx) + ", " + str(video_getter.cy) + ", " + str(video_getter.hzb))

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        corners, ids, rejected_img_points = cv2.aruco.detectMarkers(gray, self.aruco_dict, parameters=self.parameters)
        
        # If markers are detected
        if len(corners) > 0:
            # Estimate pose of each marker and return the values rvec and tvec---(different from those of camera coefficients)
            #rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[0], 0.02, matrix_coefficients, distortion_coefficients)
            # Draw a square around the markers
            #cv2.aruco.drawDetectedMarkers(frame, corners) 
            
            bbox = corners[0]
            centerW = float(bbox[0][2][0] - bbox[0][0][0]) / float(2) + float(bbox[0][0][0])
            centerH = float(bbox[0][2][1] - bbox[0][0][1]) / float(2) + float(bbox[0][0][1])
            self.center = [int(centerW), int(centerH)]

        cv2.circle(frame, self.center, radius=5, color=(0, 255, 255), thickness=-1)
        cropped_frame = self.crop(frame)
        return cropped_frame