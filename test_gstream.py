import cv2
print(cv2.__file__)
print(cv2.getBuildInformation())

cap = cv2.VideoCapture('udpsrc port=5000 ! gdpdepay ! rtph264depay ! avdec_h264 ! videoconvert ! appsink sync=false')

while True:
    ret, frame = cap.read()
    if ret:
        cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
