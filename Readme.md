nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, format=(string)NV12, framerate=(fraction)%d/1 ! nvvidconv flip-method=%d ! video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink

nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, width=(int)1280, height=(int)720, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink

nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, format=(string)NV12,                            nvvidconv flip-method=0 ! video/x-raw, width=(int)1280, height=(int)720, format=(string)I420 ! max-buffers=1 drop=true ! appsink


import cv2
print(cv2.getBuildInformation())

Python 2.7.17
OpenCV 4.1.1
GStreamer:	YES (1.14.5)

Python 3.6.9
OpenCV 4.5.3
GStreamer:	NO