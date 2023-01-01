import cv2

class RecordingManager:
    
    def __init__(self):
        self.filename = "output.mp4"
        self.isRecording = False

    def startNewRecording(self):
        print('startNewRecording')
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.foutw = cv2.VideoWriter('output-wide.mp4', fourcc, 20.0, (1920, 1080))
        self.foutz = cv2.VideoWriter('output-zoom.mp4', fourcc, 20.0, (690, 690))
        self.isRecording = True
        
    def writeFrame(self, frameFullRes, frameCropped):
        self.foutw.write(frameFullRes)
        self.foutz.write(frameCropped)
        
    def stopRecording(self):
        print('stopRecording')
        self.isRecording = False
        self.foutw.release()
        self.foutz.release()