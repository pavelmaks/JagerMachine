import gi
import os
gi.require_version("Gtk", "3.0")
gi.require_version('Gst', '1.0')
from gi.repository import Gtk, GdkPixbuf, GLib
from gi.repository import Gdk, Gst

import Jager2 as j
import cv2
import numpy as np
import threading
import time

class IdleBox(Gtk.Box):#форма сканирования qr кода
    def __init__(self, parent):
        Gtk.Box.__init__(self)


        self.frame = None
        self.scannerOn = True
        self.warning = False

        self.stack = Gtk.Overlay()
        self.add(self.stack)

        self.cap = cv2.VideoCapture("./video/v1.mp4")
        ret, self.frame = self.cap.read()
        self.image = GdkPixbuf.Pixbuf.new_from_file_at_size('disp1.png', 481, 801)
        self.image_renderer = Gtk.Image.new_from_pixbuf(self.image)
        self.stack.add_overlay(self.image_renderer)


        button = Gtk.Button(label='Нажмите, чтобы начать')
        button.set_property("opacity", 0)
        button.connect("clicked", self.onClose)  # привязка тригера на переход к qr коду

        self.stack.add_overlay(button)

        ####LABEL


        #self.label.set_markup("<span color='red' size='x-large'> Invalid code</span>")
        #self.label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.0, 1.0, 0.0, 1.0))
        #self.label.set_valign(15)
        #self.label.set_valign()


        self.update = False
        ###LABEL END

    def onOpen(self):
        print('Scanner open')
        self.show_all()

        self.update = True
        print(111)
        threading.Thread(target=self.startPreview, args=()).start()

        #self.par.openBox(self, 0)

    def onClose(self,widget):
        print('Scanner close')
        print(1)
        print(2)
        print(3)
        self.update = False
        print(4)





    def warningDissapear(self):
        self.warning = True
        print('startWarning')
        time.sleep(4)
        print('endWarning')
        self.warning = False
        self.setStatusText(0)

    def startPreview(self):
        while self.update:
            GLib.idle_add(self.showFrame)
            time.sleep(0.07)




    def showFrame(self):#демонстрация кадра на экран

        #print('tick')

        ret, self.frame = self.cap.read()
        if(ret == False):
            self.cap.release()
            self.cap = cv2.VideoCapture("./video/v1.mp4")
            ret, self.frame = self.cap.read()
        #frame = self.camera.getFrame()
        #frame = frame[0:216, 0:360]
        frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

        #overlay = cv2.imread('border.png')
        #frame = cv2.addWeighted(frame,0.8,overlay,0.1,0)

        pb = GdkPixbuf.Pixbuf.new_from_data(frame.tostring(),
                                            GdkPixbuf.Colorspace.RGB,
                                            False,
                                            8,
                                            frame.shape[1],
                                            frame.shape[0],
                                            frame.shape[2]*frame.shape[1])

        #pb = pb.rotate_simple(GdkPixbuf.PixbufRotation.COUNTERCLOCKWISE)
        #pb = pb.scale_simple(480, 800, GdkPixbuf.InterpType.NEAREST)#GdkPixbuf.InterpType.NEAREST
        self.image_renderer.set_from_pixbuf(pb.copy())

        #try:
            #while not self.stopEvent.is_set():



        #except RuntimeError:
            #print("[INFO] caught a RuntimeError")


    # def close(self):
    #     print('close scanner')
    #     self.update = False


class ApplicationWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Hello World")
        self.set_size_request(480, 800)

        self.idle = IdleBox(self)
        self.box = Gtk.Stack()

        self.add(self.box)

        self.box.add(self.idle)
    def start(self):
        self.idle.onOpen()


if __name__ == '__main__':
        window = ApplicationWindow()
        ##window.setup_objects_and_events()
        window.fullscreen()
        window.start()
        window.show_all()
        Gtk.main()
