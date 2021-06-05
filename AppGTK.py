#pavel molodec

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
import RPi.GPIO as GPIO
import configparser
#import VideoPlayer as vp


Gst.init(None)
Gst.init_check(None)

class InstructionBox(Gtk.Box):

    def __init__(self, parent):
        Gtk.Box.__init__(self)

        self.servo = None

        self.parent = parent

        self.led = j.LED()

        self.busy = False

        overlay = Gtk.Overlay()
        self.add(overlay)

        self.background = Gtk.Image.new_from_file('disp1.png')
        overlay.add(self.background)

        ####LABEL
        labelfixed = Gtk.Fixed()
        #overlay.add_overlay(labelfixed) text!!!

        labelbox = Gtk.Box()
        labelbox.set_size_request(480, 100)
        #labelbox.set_margin_start(150)
        labelbox.override_background_color(0, Gdk.RGBA(0.9, 0.9, 0.9, 1))

        self.label = Gtk.Label(label="Код неверен")
        self.setStatusText(0)
        #self.label.set_markup("<span color='red' size='x-large'> Invalid code</span>")
        #self.label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.0, 1.0, 0.0, 1.0))
        #self.label.set_valign(15)
        #self.label.set_valign()
        labelbox.add(self.label)
        labelfixed.put(labelbox, 0, 0)
        ###LABEL END

        button = Gtk.Button(label='Установите емкость и нажмите')
        button.set_property("opacity", 0)
        button.connect("clicked", self.servoGo)

        overlay.add_overlay(button)

    def onOpen(self):
        print('Instruction open')
        print(12)
        #self.servo.start()
        time.sleep(0.1)
        print(13)
        self.led.on()
        print(14)
        self.setStatusText(0)
        print(15)
        self.busy = False
        print(16)
        self.show_all()
        print(17)

    def onClose(self):
        #self.servo.close()
        print('Instruction close')

    def setStatusText(self, num):#изменение фона и надписей
        if num == 0: #0 = idle, 1 = invalid, 2 = used
            self.label.set_markup("<span color='green' size='x-large'>QR-code активирован\nУстановите емкость\nи нажмите на экран</span>")
            GLib.idle_add(self.setBackground, 0)
        elif num == 1:
            self.label.set_markup("<span color='black' size='x-large'>Процесс разлива</span>")
            GLib.idle_add(self.setBackground, 1)
        elif num == 2:
            self.label.set_markup("<span color='green' size='x-large'>Процесс разлива окончен</span>")
            GLib.idle_add(self.setBackground, 2)

    def setBackground(self, num):#изменение фона
        if num == 0:
            self.background.set_from_file("disp_start.png")
        elif num == 1:
            self.background.set_from_file("disp_fill.png")
        elif num == 2:
            self.background.set_from_file("disp_finish.png")
        #self.background.show()

    def toIdle(self):
        self.parent.openBox(self, 0)
        self.led.off()
        print("toIdle")


    def servoGo(self, widget):#запуск процесса розлива
        print(18)
        if self.busy:
            return
        print(19)
        self.setStatusText(1)
        print(20)
        self.busy = True
        print(21)
        threading.Thread(target=self.servoAct, args=()).start()

    def servoAct(self):#запуск налива и возвращение в первую форму
        print(22)
        servoTime=j.get_setting(j.path, 'Settings', 'servoTime')
        print(23)
        servo = j.ServoAct()
        print(24)
        print('servoGo')
        servo.setActPosition()
        print(25)
        time.sleep(0.4)
        print(26)
        print('servoOnPlace')
        #self.servo.hold()
        time.sleep(servoTime)

        print('servoGoHome')
        servo.setIdlePosition()
        time.sleep(0.4)

        print('servoEnd')
        servo.hold()
        time.sleep(2)

        self.setStatusText(self.setStatusText(2))

        time.sleep(7)

        self.toIdle()

    def close(self):
        self.servo.close()
        print('close instr')

class IdleBox(Gtk.Box):#стартовая форма

    def __init__(self, parent):
        Gtk.Box.__init__(self)

        self.parent = parent
        #self.videoPlayer = VideoPlayer()

        overlay = Gtk.Overlay()
        self.add(overlay)

        background = Gtk.Image.new_from_file('start.png')
        #background = Gtk.Image()
        #buf = GdkPixbuf.PixbufAnimation.new_from_file("disp1.png")
        #background.set_from_animation(buf)



        overlay.add(background)

        #player = OneMorePlayer()
        #overlay.add_overlay(player)

        #self.videoWidget = GstWidget('file:///home/pi/Documents/video')
        #self.videoWidget.set_size_request(480, 800)

        #self.gstPlayer = GstPlayer()
        #self.gstPlayer.setup_player('video.mkv')
        #self.gstPlayer.play()

        #overlay.add_overlay(self.gstPlayer)

        button = Gtk.Button(label='Нажмите, чтобы начать')
        button.set_property("opacity", 0)
        button.connect("clicked", self.toScanner) # привязка тригера на переход к qr коду

        overlay.add_overlay(button)

        """
        exitbutton = Gtk.Button(label='X')
        #exitbutton.set_property('opacity', 0)
        exitbutton.connect("clicked", parent.destroy)
        exitbutton.set_size_request(50, 50)
        
        fixed = Gtk.Fixed()
        fixed.put(exitbutton, 0, 0)
        
        overlay.add_overlay(fixed)
        
"""
    def onOpen(self):
        print('Idle open')
        self.show_all()

    def onClose(self):
        print('Idle close')

    def toScanner(self, widget): # функция перехода к QR коду
        self.parent.openBox(self, 1)

    # def close(self):
    #     print('close idle')


class OneMorePlayer(Gtk.Box):

    def __init__(self):
        Gtk.Box.__init__(self)

        self.secs = int(round(time.time() * 1000))

        self.cap = None

        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.connect("draw", self.on_drawing_area_draw)
        self.drawing_area.set_size_request(480, 800)
        self.add(self.drawing_area)

        #self.image = Gtk.Image()
        #self.image = Gtk.Image.new_from_file('disp2.png')
        #self.image.set_size_request(480, 800)
        #self.add(self.image)

        self.mymutex = threading.Lock()
        self.dimg = GdkPixbuf.Pixbuf.new_from_file('disp1.png')

        thread = threading.Thread(target = self.VideoLoop)
        #thread.daemon = True
        thread.start()
        self.show_all()

    def on_drawing_area_draw(self,widget,cr):
        #print('')
        #self.mymutex.acquire()
        #print('draw')
        Gdk.cairo_set_source_pixbuf(cr, self.dimg.copy(), 0, 0)
        cr.paint()
        now = int(round(time.time() * 1000))
        print(str(now-self.secs))
        self.secs = now
        #self.mymutex.release()

    def VideoLoop(self):

        filename = 'video.mp4'

        self.cap = cv2.VideoCapture(filename)
        print(self.cap.isOpened())

        #GLib.timeout_add(3, self.drawing_area.queue_draw)


        while True:
            #GLib.idle_add(self.showFrame)
            self.showFrame()
            time.sleep(0.03)
        #img = np.random.randint(255, size=(300, 600, 3))
        #isWritten = cv2.imwrite('image-2.png', img)

    def show(self):
        self.image.set_from_pixbuf(self.dimg.copy())

    def showFrame(self):
        #while True:
        #print('showFrame')
        ret, img = self.cap.read()

        #print(save)
        if img is not None:
            #save = cv2.imwrite('/home/pi/image-3.png', img)
            #print(save)
            #self.mymutex.acquire()
            #boxAllocation = self.drawing_area.get_allocation()
            #print(boxAllocation.width)
            #img = cv2.resize(img, (boxAllocation.width,\
            #                       boxAllocation.height))

            #img = cv2.resize(img, (480, 800))

            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) # opencv by default load BGR colorspace. Gtk supports RGB hance the conversion
            self.dimg = GdkPixbuf.Pixbuf.new_from_data(img.tostring(),
                                                  GdkPixbuf.Colorspace.RGB,False,8,
                                                  img.shape[1],
                                                  img.shape[0],                                                      img.shape[2]*img.shape[1],None,None)

            #time.sleep(0.03)

            Gdk.threads_add_idle(GLib.PRIORITY_DEFAULT_IDLE, self.drawing_area.queue_draw)
            #GLib.idle_add(self.drawing_area.queue_draw)


            #self.drawing_area.queue_draw()
            #self.drawing_area.draw()
            #self.mymutex.release()

            #time.sleep(0.1)
            if ((cv2.waitKey(30) & 0xFF) == ord('q')):
                print('off')
        else:
            #self.mymutex.release()
            print('end of file')





class ScannerBox(Gtk.Box):#форма сканирования qr кода
    def __init__(self, par):
        Gtk.Box.__init__(self)

        self.par = par

        self.camera = j.CameraCapture()

        self.qrdetect = j.QRDetect()
        self.qrcheck = j.QRCheck()
        self.frame = None
        self.scannerOn = True


        self.warning = False

        self.stack = Gtk.Overlay()
        self.add(self.stack)

        background = Gtk.Image.new_from_file('disp2.png')
        self.stack.add(background)

        self.image = GdkPixbuf.Pixbuf.new_from_file_at_size('disp1.png', 480, 800)
        self.image_renderer = Gtk.Image.new_from_pixbuf(self.image)
        self.stack.add_overlay(self.image_renderer)

        ####LABEL
        labelfixed = Gtk.Fixed()
        self.stack.add_overlay(labelfixed)

        labelbox = Gtk.Box()
        labelbox.set_size_request(480, 100)
        #labelbox.set_margin_start(150)
        labelbox.override_background_color(0, Gdk.RGBA(0.1, 0.23, 0.0, 1))

        self.label = Gtk.Label(label="Код неверен")
        #self.label.set_markup("<span color='red' size='x-large'> Invalid code</span>")
        #self.label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.0, 1.0, 0.0, 1.0))
        #self.label.set_valign(15)
        #self.label.set_valign()
        labelbox.add(self.label)
        labelfixed.put(labelbox, 0, 0)

        self.update = False
        ###LABEL END

    def onOpen(self):
        print('Scanner open')

        self.camera.start()

        self.show_all()
        self.setStatusText(0)

        self.update = True

        threading.Thread(target=self.startPreview, args=()).start()
        threading.Thread(target=self.qrCheck, args=()).start()

        #self.par.openBox(self, 0)

    def onClose(self):
        print('Scanner close')
        print(1)
        self.camera.stop()
        print(2)
        self.setStatusText(0)
        print(3)
        self.update = False
        print(4)

    def toIdle(self, widget):
        self.par.openBox(self, 0)
        print("toIdle")


    def toInstruction(self, widget):
        print(10)
        self.par.openBox(self, 2)
        print(11)
        print('toInstruction')

    def setStatusText(self, num):
        if num == 0: #0 = idle, 1 = invalid, 2 = used
            self.label.set_markup("<span foreground='#ebe6c0' weight='ultrabold' size='xx-large'>              Поднесите QR-код</span>")
        elif num == 1:
            self.label.set_markup("<span color='red' size='x-large'>     QR-code не подходит</span>")
            threading.Thread(target=self.warningDissapear, args=()).start()
        elif num == 2:
            self.label.set_markup("<span color='red' size='x-large'>     QR-code уже был использован</span>")
            threading.Thread(target=self.warningDissapear, args=()).start()
        elif num == 3:
            self.label.set_markup("<span color='green' size='x-large'>     QR-code принят</span>")
        elif num == 4:
            self.label.set_markup("<span color='green' size='x-large'>     Admin privet</span>")
        elif num == 5:
            self.label.set_markup("<span color='green' size='x-large'>     Destroy</span>")
            time.sleep(4)
        elif num == 6:
            self.label.set_markup("<span color='green' size='x-large'>     Настройки изменены</span>")
            time.sleep(3)
        elif num > 6:
            self.label.set_markup("<span color='green' size='x-large'>     Проливка "+str(num)+" секунд</span>")
            time.sleep(3)



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
            time.sleep(0.1)

    def qrCheck(self):#функция проверки qr кода и выдачи результата

        time.sleep(1)

        start_time = time.time()

        while self.update:
            if self.frame is not None:

                print('CHECK QR')

                qrdata = self.qrdetect.detect(self.frame)

                if time.time()-start_time > 30:
                    self.update = False
                    time.sleep(0.5)
                    self.toIdle(None)

                if qrdata is not None:
                    qrresult = self.qrcheck.check(qrdata)
                    if qrresult == -1:
                        print("Invalid code")
                        if not self.warning:
                            self.setStatusText(1)
                            #4 sec wait

                    elif qrresult == -2:
                        print("Code already used")
                        if not self.warning:
                            self.setStatusText(2)
                            #4 sec wait
                    elif qrresult == -3:
                        print("Admin privet")
                        time.sleep(1)
                        if not self.warning:
                            self.setStatusText(4)
                    elif qrresult == -4:
                        global m
                        print("Destroy")
                        time.sleep(1)
                        if not self.warning:
                            self.setStatusText(5)
                        self.update = False
                        self.par.close()
                    elif qrresult == -5:
                        print("Settings")
                        time.sleep(1)
                        if not self.warning:
                            self.setStatusText(6)
                        time.sleep(10)
                        if not self.warning:
                            self.setStatusText(0)
                        start_time = time.time()



                    elif qrresult < -6:
                        print("Proliv")
                        time.sleep(1)
                        if not self.warning:
                            self.setStatusText(-qrresult)

                        servo = j.ServoAct()
                        servo.setActPosition()
                        time.sleep(0.4)
                        time.sleep(-qrresult)
                        servo.setIdlePosition()
                        time.sleep(0.4)
                        servo.hold()
                        time.sleep(2)
                        start_time = time.time()
                        if not self.warning:
                            self.setStatusText(0)


                    elif qrresult == 1:
                        print("Code is valid")
                        self.setStatusText(3)
                        self.qrcheck.applyLast()
                        self.update = False

                        time.sleep(0.5)
                        self.toInstruction(None)
                        #Servo go

            time.sleep(0.5)

        self.qrcheck.close()


    def showFrame(self):#демонстрация кадра на экран

        #print('tick')
        frame = self.camera.getFrame()
        frame = frame[0:216, 0:360]
        #frame = cv2.resize(frame, (800, 480))
        self.frame = frame.copy()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame,1)

        #overlay = cv2.imread('border.png')
        #frame = cv2.addWeighted(frame,0.8,overlay,0.1,0)

        pb = GdkPixbuf.Pixbuf.new_from_data(frame.tostring(),
                                            GdkPixbuf.Colorspace.RGB,
                                            False,
                                            8,
                                            frame.shape[1],
                                            frame.shape[0],
                                            frame.shape[2]*frame.shape[1])

        pb = pb.rotate_simple(GdkPixbuf.PixbufRotation.COUNTERCLOCKWISE)
        pb = pb.scale_simple(480, 800, GdkPixbuf.InterpType.NEAREST)#GdkPixbuf.InterpType.NEAREST
        self.image_renderer.set_from_pixbuf(pb.copy())

        #try:
            #while not self.stopEvent.is_set():



        #except RuntimeError:
            #print("[INFO] caught a RuntimeError")


    # def close(self):
    #     print('close scanner')
    #     self.update = False


class AppWindow(Gtk.Window):#главная форма
    def __init__(self):


        Gtk.Window.__init__(self, title="Hello World")
        self.set_size_request(480, 800)

        self.idle = IdleBox(self)
        self.scanner = ScannerBox(self)
        self.instruct = InstructionBox(self)

        self.box = Gtk.Stack()

        self.add(self.box)

        self.box.add(self.idle)


        """
        self.overlay = Gtk.Overlay()
        self.add(self.overlay)
        self.background = Gtk.Image.new_from_file('disp1.png')
       
        self.button = Gtk.Button(label='Test')
        self.button.set_property("opacity", 0.1)
        self.button.connect("clicked", self.on_button_clicked)
        self.overlay.add(self.background)
        self.overlay.add_overlay(self.button)
        """

    #def close(self):
    #    self.instruct.close()

    def destroySafe(self):
        Gtk.main_quit()
        self.idle.close()
        self.scanner.close()
        self.instruct.close()

    def destroy(self):
        GLib.idle_add(self.destroySafe)


    def openBoxSafe(self, widget, num):
        #0 - idle, 1 - scanner, 2 - instruct
        self.box.remove(widget)

        widget.onClose()
        target = None

        if num == 0:
            target = self.idle
            print('0')
        elif num == 1:
            target = self.scanner
            print('1')
        elif num == 2:
            target = self.instruct
            print('2')

        self.box.add(target)
        target.onOpen()

        #self.box.remove(target)
        #self.show_all()

    def openBox(self, widget, num):
        GLib.idle_add(self.openBoxSafe, widget, num)

    def on_button_clicked(self, widget):
        print("Hello World")
        #win = ScannerWindow()
        #win.show_all()
        self.button.destroy()
        #

class main:
    def __init__(self): #консруктор
        self.win = AppWindow()
        self.win.connect("destroy", self.close)
        self.win.fullscreen()
        self.win.show_all()
        Gtk.main()

    def close(self, widget):
         Gtk.main_quit()
         self.win.close()
         # self.win.scanner.close()
         # self.win.instruct.close()


m = main()

