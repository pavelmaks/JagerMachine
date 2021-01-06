import Jager2 as j
import cv2
import numpy as np
import imutils
from tkinter import *
from PIL import Image, ImageTk
import time
import threading
import os      

class IdleWindow():
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.button1 = Button(self.frame, text = 'toScanner', width = 25, command = self.toScanner)
        self.button1.pack()
        self.frame.pack()
        
    def toScanner(self):
        self.newWindow = Toplevel(self.master)
        #self.newWindow.attributes('-fullscreen', True)
        self.newWindow.geometry('480x800')
        self.app = CameraWindow(self.newWindow)
        #self.master.destroy()

class CameraWindow():
    def __init__(self, master):
        
        self.master = master
        self.frame = Frame(self.master)
        self.panel = Label(self.frame)
        self.panel.bind("<1>", self.toIdle)
        self.panel.pack()
               
        self.frame.pack()
   
        self.can = Canvas(self.master, width=400, height=400)
        self.can.create_text(
            20, 60, anchor=W, font="Arial",
            text="На пылающий город падает тень"
        )
        self.can.place(x=20, y=20)
   
        self.qrdetect = j.QRDetect()
        self.qrcheck = j.QRCheck()
        self.invalidQr = False
        self.usedQr = False
   
   
        self.camera = j.CameraCapture()
        self.camera.start()
               
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.showFrame, args=())
        self.thread.start()
    
    
    def cameraCapture(self):
        print('Start Camera Capture')  
        frame = self.camera.getFrame()
        self.cameraWindow.showFrame(frame)
    
    def showFrame(self):
        
        try:
            while not self.stopEvent.is_set():
            
                frame = self.camera.getFrame()
                frame = frame[0:216, 0:360]
                
                qrdata = self.qrdetect.detect(frame)
                if qrdata is not None:
                    qrresult = self.qrcheck.check(qrdata)
                    if qrresult == -1:
                        print("Invalid code")
                        self.invalidQr = True
                        #4 sec wait
                        
                    elif qrresult == -2:
                        print("Code already used")
                        self.usedQr = True
                        #4 sec wait
                        
                    elif qrresult == 1:
                        print("Code is valid")
                        #Servo go
                
                #frame = cv2.rotate(frame,cv2.ROTATE_90_CLOCKWISE)
                #frame = imutils.resize(frame, width=800, inter=cv2.INTER_NEAREST)
                
                if self.invalidQr:
                    t=0
                    #cv2.putText(frame, 'Invalid code', (240, 700), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                if self.usedQr:
                    t=0
                    #cv2.putText(frame, 'Already used', (240, 700), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = image.resize((800, 480), Image.ANTIALIAS)
                image = image.transpose(Image.ROTATE_90)
                image = ImageTk.PhotoImage(image)
                  
                self.panel.configure(image=image)
                self.panel.image = image
                
        except RuntimeError:
            print("[INFO] caught a RuntimeError")
            
        
    def toIdle(self, event):
        self.onClose()
        self.newWindow = Toplevel(self.master)
        #self.newWindow.attributes('-fullscreen', True)
        self.newWindow.geometry('480x800')
        self.app = IdleWindow(self.newWindow)
        

        
        
    def onClose(self):
        self.stopEvent.set()
        self.camera.stop()
        self.master.destroy()
        


"""
class App:
    def __init__(self):
        
        self.camera = j.CameraCapture()
        self.qrdetect = j.QRDetect()
        self.qrcheck = j.QRCheck()
        self.servo = j.ServoAct()
"""

    
def main():
    root = Tk()
    root.geometry('480x800')
    #root.wm_attributes('-alpha', 0.5)
    #root.attributes('-fullscreen', True)  
    app = IdleWindow(root)
    root.mainloop()

main()

"""
class Main:
    def __init__(self):
        self.camera = j.CameraCapture()
        self.window = Tk()
        self.window.attributes('-fullscreen', True)  
        self.fullScreenState = False
        
        self.window.bind("<F11>", self.toggleFullScreen)
        self.window.bind("<Escape>", self.quitFullScreen)
    
        self.b1 = Button(text="Изменить", width=30, height=3)
        self.b1['command'] = self.onClick1
        
        self.b1.pack()
        
        self.window.mainloop()

   
    def cameraCapture(self):
        print('Start Camera Capture')  
        frame = self.camera.getFrame()
        self.cameraWindow.showFrame(frame)
    

    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.window.attributes("-fullscreen", self.fullScreenState)

    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.window.attributes("-fullscreen", self.fullScreenState)


fe = Fullscreen_Example()
"""

    
