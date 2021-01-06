from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import re

detector = cv2.QRCodeDetector()

camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    img = frame.array

    key = cv2.waitKey(1) & 0xFF
     
    
    data, bbox, _ = detector.detectAndDecode(img)
    
    if bbox is not None:
            
        for i in range(len(bbox)):
            cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255, 0, 0), thickness=2)
            
        cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1])-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        
        if data:
            print('Data found: ' + data)
            data = ''
         
    #cv2.imshow('code detector', img)     
     
    img = cv2.resize(img, (640, 480))
    
    cv2.imshow("Frame", img) 
     
    rawCapture.truncate(0)
        
    if key == ord("q"):
        break


#cap = cv2.VideoCapture(0)
#detector = cv2.QRCodeDetector()

#while True:
       
    
       
    #_, img = cap.read()
    #data, bbox, _ = detector.detectAndDecode(img)
    
    """
    if bbox is not None:
            
        for i in range(len(bbox)):
            cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255, 0, 0), thickness=2)
            
        cv.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1])-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        
        if data:
            print('Data found: ' + data)
            data = ''
         
    cv2.imshow('code detector', img)
      """