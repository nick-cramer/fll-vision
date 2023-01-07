from tkinter import *
from PIL import ImageTk, Image
import cv2

class UI:
    
    def __init__(self):
        self.root = Tk()
        self.root.title('FLL Vision')
        self.root.state('zoomed')
        self.mode = "READY"  # RECORDING, REPLAYING


    def startRecordingMode(self):
        self.countdown_timer.start()
        self.rec_mgr.startNewRecording()

    def startInstantReplayMode(self):
        self.countdown_timer.stop()
        self.rec_mgr.stopRecording()
        self.replay_getter.open()



    def resetMode(self):
        self.countdown_timer.reset()
        self.replay_getter.close()


    def button_press(self):
        print("button_press!")
        if self.mode == 'READY':
            self.gobutton.config(text='Stop')
            self.startRecordingMode()
            self.mode = 'RECORDING'
        elif self.mode == 'RECORDING':
            self.gobutton.config(text='Reset')
            self.startInstantReplayMode()
            self.mode = 'REPLAYING'
        elif self.mode == 'REPLAYING':
            self.gobutton.config(text='Start')
            self.resetMode()
            self.mode = 'READY'

    def init(self, video_getter, countdown_timer, rec_mgr, robot_tracker, replay_getter):
    
        self.webcam = video_getter
        self.zoomh = video_getter.zoomh
        self.countdown_timer = countdown_timer
        self.rec_mgr = rec_mgr
        self.robot_tracker = robot_tracker
        self.replay_getter = replay_getter



        app = Frame(self.root, bg="white")
        app.grid()

        self.runsview = Frame(app, bg="white")
        self.runsview.grid()

        # Create a label in the frame
        self.vidmain = Label(app, width=1230, height=690, borderwidth=1, relief="solid")
        self.vidzoom = Label(app, width=690, height=690, borderwidth=1, relief="solid")

        self.gobutton = Button(app, text="Start", width=20, command=self.button_press)

        history = Listbox(self.runsview)
        history.insert(1, "Current Activity")
        history.insert(2, "Friday, 2:00 pm, December 23, 2022")
        history.insert(3, "Friday, 2:00 pm, December 22, 2022")
        history.insert(4, "Friday, 2:00 pm, December 21, 2022")
        history.insert(5, "Friday, 2:00 pm, December 20, 2022")
        
        stats = Listbox(self.runsview)
        stats.insert(1, "Home, 15 seconds")
        stats.insert(2, "Run, 55 seconds, Distance Traveled: 92 cm, Avg speed: 25 cm/s")
        stats.insert(3, "Home, 32 seconds")
        stats.insert(4, "Run, 55 seconds, Distance Traveled: 192 cm, Avg speed: 18 cm/s")

        self.runsview.columnconfigure(0, weight=1)
        self.runsview.columnconfigure(1, weight=1)

        self.timer = Label(app, text="2:30", borderwidth=0, relief="solid", font=("Arial", 72), bg="white")

        history.grid(row=0, column=0, sticky=(N, S, E, W))
        stats.grid(row=0, column=1, sticky=(N, S, E, W))

        self.vidmain.grid(row=0, column=0)
        self.vidzoom.grid(row=0, column=1)
        self.runsview.grid(row=1, column=0, sticky=(N, S, E, W))
        self.timer.grid(row=1, column=1, sticky=(N, S, E, W))
        self.gobutton.grid(row=2, column=1, pady=20)


    def display(self, frameFullRes, frameCropped):
    
        if self.rec_mgr.isRecording:
            self.rec_mgr.writeFrame(frameFullRes, frameCropped)

        img = Image.fromarray(cv2.cvtColor(frameFullRes, cv2.COLOR_BGR2RGB)).resize((1230, 690))
        imgtk = ImageTk.PhotoImage(image=img)
        #cps.increment()
        #print("CPS: " + str(cps.countsPerSec()))

        imgCropped = Image.fromarray(cv2.cvtColor(frameCropped, cv2.COLOR_BGR2RGB)).resize((690, 690), Image.ANTIALIAS)
        imgtkCropped = ImageTk.PhotoImage(image=imgCropped)

        self.vidzoom.imgtk = imgtkCropped
        self.vidzoom.configure(image=imgtkCropped) 

        self.vidmain.imgtk = imgtk
        self.vidmain.configure(image=imgtk)


    def show_frame_loop(self, video_getter, replay_getter):

        if self.mode == 'REPLAYING':
            frameFullRes = replay_getter.getNextFullResFrame()
            frameCropped = replay_getter.getNextCroppedFrame()
        else:
            frameFullRes = video_getter.frame
            frameCropped = self.robot_tracker.crop_to_robot(frameFullRes, video_getter)

        self.display(frameFullRes, frameCropped)        
        self.root.after(100, self.show_frame_loop, video_getter, replay_getter)

    def update_time(self, time_label):
        self.timer.config(text=time_label)