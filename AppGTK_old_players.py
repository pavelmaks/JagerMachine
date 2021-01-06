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
#import VideoPlayer as vp

Gst.init(None)
Gst.init_check(None)

class InstructionBox(Gtk.Box):
 
    def __init__(self, parent):
        Gtk.Box.__init__(self)
        
        self.servo = j.ServoAct()
        
        self.parent = parent
        
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
        #self.servo.start()
        time.sleep(0.1)
        self.setStatusText(0)
        self.busy = False
        self.show_all()
     
    def onClose(self):
        #self.servo.close()
        print('Instruction close')
        
    def setStatusText(self, num):
        if num == 0: #0 = idle, 1 = invalid, 2 = used
            self.label.set_markup("<span color='green' size='x-large'>QR-code активирован\nУстановите емкость\nи нажмите на экран</span>")
            GLib.idle_add(self.setBackground, 0)
        elif num == 1:
            self.label.set_markup("<span color='black' size='x-large'>Процесс разлива</span>")
            GLib.idle_add(self.setBackground, 1)
        elif num == 2:        
            self.label.set_markup("<span color='green' size='x-large'>Процесс разлива окончен</span>")
            GLib.idle_add(self.setBackground, 2)
  
    def setBackground(self, num):
        if num == 0:
            self.background.set_from_file("disp_start.png")
        elif num == 1:
            self.background.set_from_file("disp_fill.png")
        elif num == 2:
            self.background.set_from_file("disp_finish.png")
        #self.background.show()

    def toIdle(self):
        self.parent.openBox(self, 0)
        print("toIdle")


    def servoGo(self, widget):
        
        if self.busy:
            return
        
        self.setStatusText(1)
        self.busy = True
        threading.Thread(target=self.servoAct, args=()).start()

    def servoAct(self):
        print('servoGo')
        self.servo.setActPosition()
        time.sleep(0.4)
        
        print('servoOnPlace')
        #self.servo.hold()
        time.sleep(6)
        
        print('servoGoHome')
        self.servo.setIdlePosition()
        time.sleep(0.4)
        
        print('servoEnd')
        self.servo.hold()
        time.sleep(2)
        self.setStatusText(self.setStatusText(2))
        
        time.sleep(7)
        
        self.toIdle()
        
    def close(self):
        self.servo.close()
        print('close instr')

class IdleBox(Gtk.Box):
    
    def __init__(self, parent):   
        Gtk.Box.__init__(self)
        
        self.parent = parent
        #self.videoPlayer = VideoPlayer()
        
        overlay = Gtk.Overlay()
        self.add(overlay)    
        
        background = Gtk.Image.new_from_file('disp1.png')
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
        button.connect("clicked", self.toScanner)
          
        overlay.add_overlay(button)
        
        """
        exitbutton = Gtk.Button(label='')
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

    def toScanner(self, widget):
        self.parent.openBox(self, 1)

    def close(self):
        print('close idle')

"""
class OneMorePlayer(Gtk.Box):
    
    
    def __init__(self):
        Gtk.Box.__init__(self)        
       
        self.cap = None
       
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_size_request(480, 800)
        #self.add(self.drawing_area)
       
        self.image = Gtk.Image()
        self.image.set_size_request(480, 800)
        self.add(self.image)
       
        #self.mymutex = threading.Lock()
        self.dimg = GdkPixbuf.Pixbuf.new_from_file('disp2.png')
        
        thread = threading.Thread(target = self.VideoPlayerDA)
        #thread.daemon = True
        thread.start()
        
   
        
        
    def on_drawing_area_draw(self,widget,cr):
        mymutex.acquire()
        Gdk.cairo_set_source_pixbuf(cr, self.dimg.copy(), 0, 0)
        cr.paint()
        mymutex.release()
       
    def VideoLoop(self):
        
        filename = 'video.mp4'
        
    
        self.cap = cv2.VideoCapture(filename)
        print(cap.isOpened())
        
        while True:
            GLib.idle_add(self.VideoPlayerDA)
            time.sleep(0.2)
        
    def VideoPlayerDA(self):
    
       drawing_area = self.drawing_area

          while True:
            
            #self.mymutex.acquire()
            ret, img = cap.read()
            if img is not None:
                
                boxAllocation = drawing_area.get_allocation()
                #print(boxAllocation.width)
                img = cv2.resize(img, (boxAllocation.width,\
                                       boxAllocation.height))

                img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) # opencv by default load BGR colorspace. Gtk supports RGB hance the conversion
                self.dimg = GdkPixbuf.Pixbuf.new_from_data(img.tostring(),
                                                      GdkPixbuf.Colorspace.RGB,False,8,
                                                      img.shape[1],
                                                      img.shape[0],
                                                      img.shape[2]*img.shape[1],None,None)

                #time.sleep(0.03)
                self.image.set_from_pixbuf(self.dimg.copy())
                
                #drawing_area.queue_draw()
                #self.mymutex.release()
                
                time.sleep(0.03)
                #if ((cv2.waitKey(30) & 0xFF) == ord('q')):
                #    break
            else:
                #self.mymutex.release()
                break
        print('end of file')
"""    
    
    
    

class Player(Gtk.Box):
    
    def __init__(self):
        Gtk.Box.__init__(self)
        self.xid = None
        self.drawingarea = None
        self.pipeline = None
        self.bus = None
        self.playbin = None
        
    def init(self):
        self.drawingarea = Gtk.DrawingArea.new()
        self.drawingarea.connect('draw', self.on_draw)
        self.drawingarea.connect('realize', self.on_realize)
        self.drawingarea.connect('unrealize', self.on_unrealize)
        self.drawingarea.set_size_request(480, 800)
        
         # Create GStreamer pipeline
        self.pipeline = Gst.Pipeline()

        # Create bus to get events from GStreamer pipeline
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message::eos', self.on_eos)
        self.bus.connect('message::error', self.on_error)

        # This is needed to make the video output in our DrawingArea:
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message::element', self.on_sync_message)

        # Create GStreamer elements
        self.playbin = Gst.ElementFactory.make('playbin', None)

        # Add playbin to the pipeline
        self.pipeline.add(self.playbin)

        # Set properties
        uri = "file://" + os.path.abspath('video.mp4')
        self.playbin.set_property('uri', uri)
       
    def play(self):
        self.pipeline.set_state(Gst.State.PLAYING)
    
    def on_draw(self, widget, cr):
        print("ondraw", self.playbin.get_state(0).state)
        if self.playbin.get_state(0).state < Gst.State.PAUSED:
            allocation = widget.get_allocation()

            cr.set_source_rgb(0, 0, 0)
            cr.rectangle(0, 0, allocation.width, allocation.height)
            cr.fill()

#       self.on_realize(widget)

    def on_realize(self, widget, data=None):
        print("on_relaize")

        window = widget.get_window()
        self.xid = window.get_xid()

    def on_unrealize(self, widget, data=None):
        # to prevent racing conditions when closing the window while playing
        self.playbin.set_state(Gst.State.NULL)
        self.pipeline.set_state(Gst.State.NULL)

    def on_sync_message(self, bus, msg):
        if msg.get_structure().get_name() == 'prepare-window-handle':
            print('prepare-window-handle')

            print('on_sync', self.xid)
            self.playbin.set_window_handle(self.xid)

            print(msg)
            print(msg.src)


    def on_eos(self, bus, msg):
        print('on_eos(): seeking to start of video')
        self.pipeline.seek_simple(
            Gst.Format.TIME,
            Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,
            0
        )

    def on_error(self, bus, msg):
        print('on_error():', msg.parse_error())
       

class GstPlayer(Gtk.Box):

    def __init__(self):

        # init GStreamer
        #Gst.init(None)

        # setting up builder
        #builder = Gtk.Builder()
        #builder.add_from_file("23_gtksink_player.glade")
        #builder.connect_signals(Handler())

        #self.movie_window = builder.get_object("play_here")
        #self.playpause_button = builder.get_object("playpause_togglebutton")
        #self.slider = builder.get_object("progress")
        #self.slider_handler_id = self.slider.connect("value-changed", self.on_slider_seek)

        # setting up videoplayer
        self.player = Gst.ElementFactory.make("playbin", "player")
        #self.sink = Gst.ElementFactory.make("gtksink")
        self.sink = Gst.ElementFactory.make('gtksink')
        print(self.sink)
        # setting up media widget
        video_widget = self.sink.get_property("widget")
        self.add(video_widget)
        #builder.get_object("video_box").add(video_widget)

        #window = builder.get_object("window")
        #window.show_all()

    def setup_player(self, f):
        # file to play must be transmitted as uri
        uri = "file://" + os.path.abspath(f)
        self.player.set_property("uri", uri)
        self.player.set_property("video-sink", self.sink)

    def play(self):
        self.is_playing = True
        self.player.set_state(Gst.State.PLAYING)
        # starting up a timer to check on the current playback value
        #GLib.timeout_add(1000, self.update_slider)

    def pause(self):
        self.is_playing = False
        self.player.set_state(Gst.State.PAUSED)

    def current_position(self):
        status,position = self.player.query_position(Gst.Format.TIME)
        return position

    def clear_playbin(self):
        try:
            self.player.set_state(Gst.State.NULL)
        except:
            pass

    def main(self):
        Gtk.main()



class GstWidget(Gtk.Box):
    def __init__(self, pipeline):
        super().__init__()
        self.connect('realize', self._on_realize)
        video_src = 'file:///home/pi/Documents/video'
        self._bin = Gst.parse_bin_from_description(video_src, True)

    def _on_realize(self, widget):
        pipeline = Gst.Pipeline()
        factory = pipeline.get_factory()
        gtksink = factory.make('gtksink')
        print(gtksink)
        pipeline.add(gtksink)
        pipeline.add(self._bin)
        self._bin.link(gtksink)
        self.pack_start(gtksink.props.widget, True, True, 0)
        gtksink.props.widget.show()
        pipeline.set_state(Gst.State.PLAYING)



class ScannerBox(Gtk.Box):
    def __init__(self, parent):
        Gtk.Box.__init__(self)
        
        self.parent = parent
        
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
        labelbox.override_background_color(0, Gdk.RGBA(0.9, 0.9, 0.9, 1))
               
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
 
        #self.parent.openBox(self, 0)
              
    def onClose(self):
        print('Scanner close')
        self.camera.stop()
        self.setStatusText(0)
        self.update = False

    def toIdle(self, widget):
        self.parent.openBox(self, 0)
        print("toIdle")
    
    
    def toInstruction(self, widget):
        self.parent.openBox(self, 2)
        print('toInstruction')
    
    def setStatusText(self, num):
        if num == 0: #0 = idle, 1 = invalid, 2 = used
            self.label.set_markup("<span color='black' size='x-large'> Поднесите QR-код</span>")
        elif num == 1:
            self.label.set_markup("<span color='red' size='x-large'>QR-code не подходит</span>")
            threading.Thread(target=self.warningDissapear, args=()).start()
        elif num == 2:
            self.label.set_markup("<span color='red' size='x-large'> QR-code уже был использован</span>")
            threading.Thread(target=self.warningDissapear, args=()).start()
        elif num == 3:
            self.label.set_markup("<span color='green' size='x-large'> QR-code принят</span>")
    
    
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

    def qrCheck(self):
        
        time.sleep(1)
        
        while self.update:   
            if self.frame is not None:
            
                print('CHECK QR')
            
                qrdata = self.qrdetect.detect(self.frame)
                   
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
                

    def showFrame(self):
        
        #print('tick')
        frame = self.camera.getFrame()
        frame = frame[0:216, 0:360]
        #frame = cv2.resize(frame, (800, 480))
        self.frame = frame.copy()  
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
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
         
         
    def close(self):
        print('close scanner')
        self.update = False
        
     
class AppWindow(Gtk.Window):
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

    def close(self):
        self.instruct.close()

    def destroySafe(self):
        Gtk.main_quit()

    def destroy(self, widget, data=None):
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
    def __init__(self):
        self.win = AppWindow()
        self.win.connect("destroy", self.close)
        self.win.fullscreen()
        self.win.show_all()
        Gtk.main()
        
    def close(self, widget):
        Gtk.main_quit()
        self.win.idle.close()
        self.win.scanner.close()
        self.win.instruct.close()
        
        
m = main()

