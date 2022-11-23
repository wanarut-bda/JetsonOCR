import cv2
# import pytesseract
import easyocr
import numpy as np
gui = True
reg = True
ratio = 7

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

video = cv2.VideoCapture("test_video.mp4")
#video = cv2.VideoCapture(0) # for using CAM

# Exit if video not opened.
if not video.isOpened():
    print("Could not open video")
    exit()

# Read first frame.
ok, frame = video.read()
# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
if not ok:
    print ('Cannot read video file')
    exit()

# options = '-c tessedit_char_whitelist=0123456789'
options = '-l eng --oem 1 --psm 7 -c tessedit_char_whitelist=0123456789/()'
required = '0123456789/()'

if reg :
    reader = easyocr.Reader(['en'], gpu=True)

# ref_bbox = [346, 133, 53, 36]   # 96
# ref_bbox = [647, 141, 50, 33]   # 99
# ref_bbox = [349, 372, 47, 29]   # 136
# ref_bbox = [639, 372, 55, 34]   # 121

ref_boxs = [[346, 133, 53, 36], [346, 133, 53, 36], [647, 141, 50, 33], [344, 372, 50, 29], [639, 372, 55, 34], [658, 445, 36, 25], [344, 372, 50, 29], [344, 372, 50, 29]]

# Uncomment the line below to select a different bounding box
# ref_bbox = cv2.selectROI(frame, False)
# ref_boxs = [ref_bbox]
# for x in ref_bbox:
#     print(x)

tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
tracker_type = tracker_types[7]
trackers = []
for bbox in ref_boxs:
    p1 = (int(bbox[0]), int(bbox[1]))
    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
    roi = frame.copy()
    cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)

    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        elif tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        elif tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        elif tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        elif tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        elif tracker_type == 'GOTURN':
                tracker = cv2.TrackerGOTURN_create()
        elif tracker_type == 'MOSSE':
            tracker = cv2.TrackerMOSSE_create()
        elif tracker_type == "CSRT":
            tracker = cv2.TrackerCSRT_create()
    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)
    trackers.append(tracker)

if gui :
    cv2.imshow('frame',frame)
    cv2.waitKey()
    cv2.destroyAllWindows()
# exit()

fps = 0

while True:

    # Read a new frame
    ok, frame = video.read()
    if not ok:
        break
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Start timer
    timer = cv2.getTickCount()

    for i, tracker in enumerate(trackers):
        ocr_text = ''
        # Update tracker
        ok, bbox = tracker.update(frame)

        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            roi = frame.copy()
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)

            roi = roi[int(bbox[1]):int(bbox[1] + bbox[3]), int(bbox[0]):int(bbox[0] + bbox[2])]
            img_erosion = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            # img_erosion = roi.copy()
            kernel = np.ones((1,1), np.uint8)

            img_erosion = cv2.bitwise_not(img_erosion)

            if reg :
                try:
                    original = ''
                    # original = pytesseract.image_to_string(img_erosion, config=options)
                    results = reader.readtext(img_erosion, detail=1, allowlist=required, min_size=img_erosion.shape[0]*0.75)
                    for box, text, conf in results:
                        try:
                            cv2.rectangle(img_erosion, box[0], box[2], 255, 2, 1)
                        except:
                            pass
                        # cv2.putText(img_erosion, str(bbox[2]), box[0], cv2.FONT_HERSHEY_SIMPLEX, 0.2, (0,0,255), 1)
                        original = text
                    # if (len(result)):
                    #     original = result[0]

                    final = ''
                    for c in original:
                        for ch in required:
                            if c==ch:
                                final = final + c

                    if (final != ''):
                        # print('OCR:', final)
                        ocr_text = final

                except RuntimeError as timeout_error:
                    # Tesseract processing is terminated
                    pass

            if gui :
                roi = cv2.resize(roi, (0,0), fx=ratio, fy=ratio)
                img_erosion = cv2.resize(img_erosion, (300,200))
                cv2.putText(img_erosion, "OCR: " + ocr_text, (1,30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, 0, 2)
                cv2.imshow("img_erosion_" + str(i), img_erosion)
            print(i, ':', ocr_text)
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)



    # Exit if ESC pressed
    if cv2.waitKey(1) & 0xFF == ord('q'): # if press SPACE bar
        break

    # Calculate Frames per second (FPS)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    print('fps :', fps)
    print('-----------------------')
    
    # Display result
    if gui :
        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, 0,2)
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(fps), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, 0, 2)
        cv2.imshow("Tracking", frame)

video.release()
cv2.destroyAllWindows()