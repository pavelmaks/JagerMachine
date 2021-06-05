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


cap = cv2.VideoCapture("./video/1.mp4")
ret, frame = cap.read()
while(1):
   ret, frame = cap.read()
   cv2.imshow('frame',frame)
   if cv2.waitKey(1) & 0xFF == ord('q') or ret==False :
       cap.release()
       cv2.destroyAllWindows()
       break
   cv2.imshow('frame',frame)