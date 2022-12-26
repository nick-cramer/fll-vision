from tkinter import *
from PIL import ImageTk, Image
import cv2

class UI:
    
    def __init__(self):
        self.root = Tk()
        self.root.title('FLL Vision')
        self.root.state('zoomed')

    def init(self, video_getter):
    
        app = Frame(self.root, bg="white")
        app.grid()

        self.webcam = video_getter
        self.zoomh = video_getter.zoomh

        # Create a label in the frame
        self.vidmain = Label(app, height=video_getter.h, borderwidth=1, relief="solid")
        self.vidzoom = Label(app, width=video_getter.zoomw, height=video_getter.zoomh, borderwidth=1, relief="solid")

        history = Listbox(app)
        history.insert(1, "Current Activity")
        history.insert(2, "Friday, 2:00 pm, December 23, 2022")
        history.insert(3, "Friday, 2:00 pm, December 22, 2022")
        history.insert(4, "Friday, 2:00 pm, December 21, 2022")
        history.insert(5, "Friday, 2:00 pm, December 20, 2022")
    #
        stats = Listbox(app)
        stats.insert(1, "Home, 15 seconds")
        stats.insert(2, "Run, 55 seconds, Distance Traveled: 92 cm, Avg speed: 25 cm/s")
        stats.insert(3, "Home, 32 seconds")
        stats.insert(4, "Run, 55 seconds, Distance Traveled: 192 cm, Avg speed: 18 cm/s")

        self.timer = Label(app, text="2:30", borderwidth=1, relief="solid", font=("Arial", 72))

        self.vidmain.grid(row=0, column=0, columnspan=2)
        self.vidzoom.grid(row=0, column=2)
        history.grid(row=1, column=0, sticky=(N, S, E, W))
        stats.grid(row=1, column=1, sticky=(N, S, E, W))
        self.timer.grid(row=1, column=2, sticky=(N, S, E, W))


    def display(self, cv2image, cropped):
    
        img = Image.fromarray(cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGB))
        imgtk = ImageTk.PhotoImage(image=img)
        #cps.increment()
        #print("CPS: " + str(cps.countsPerSec()))

        imgCropped = Image.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)).resize((self.zoomh, self.zoomh)) #,Image.ANTIALIAS)
        imgtkCropped = ImageTk.PhotoImage(image=imgCropped)

        self.vidzoom.imgtk = imgtkCropped
        self.vidzoom.configure(image=imgtkCropped) 

        self.vidmain.imgtk = imgtk
        self.vidmain.configure(image=imgtk)

    def update_time(self, time_label):
        self.timer.config(text=time_label)