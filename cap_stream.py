import cv2

def gstreamer_pipeline(device, capture_width, capture_height, framerate, display_width, display_height):
    return " v4l2src device=/dev/video"+ str(device) + " !" +\
            " video/x-raw," +\
            " width=(int)" + str(capture_width) + "," +\
            " height=(int)" + str(capture_height) + "," +\
            " framerate=(fraction)" + str(framerate) +"/1 !" +\
            " videoconvert ! videoscale !" +\
            " video/x-raw," +\
            " width=(int)" + str(display_width) + "," +\
            " height=(int)" + str(display_height) + " ! appsink"

# pipeline parameters
capture_width = 1280 
capture_height = 720 
display_width = 640 
display_height = 360 
framerate = 30 

# pipeline = gstreamer_pipeline(0, capture_width, capture_height, framerate, display_width, display_height)
pipeline = 'udpsrc port=5000 ! gdpdepay ! rtph264depay ! avdec_h264 ! videoconvert ! appsink sync=false'
print(pipeline)

cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
# Check if camera opened successfully
if (not cap.isOpened()): 
    print("Error opening video stream or file")

# Read until video is completed
while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:
        cv2.imshow('frame', frame)

        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

# When everything done, release the video capture object
cap.release()
# Closes all the frames
cv2.destroyAllWindows()