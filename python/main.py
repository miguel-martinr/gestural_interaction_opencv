import numpy as np
import cv2
import bg_substractor as bg_subst

learning_rate = -1






cap = cv2.VideoCapture("http://192.168.1.51:4747/mjpegfeed?640x480")



if not cap.isOpened():
    print('Unable to open cam')
    exit(0)


# Roi
up_left = (350, 150)
down_right = (550, 350)



# launch_learning_rate_trackbar()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame. Exiting...")
        exit(0)

    frame = cv2.flip(frame, 1)
    roi = frame[up_left[1]:down_right[1], 
        up_left[0]:down_right[0], :]

    
    cv2.rectangle(frame, up_left, down_right, (255,0,0))
    cv2.imshow('Frame', frame)
    
    # Substracting background
    fg_mask = bg_subst.apply(roi)

    # Thresholding
    ret, thresh = cv2.threshold(fg_mask, 127, 255, cv2.THRESH_BINARY)
    
    # Finding contours
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    cv2.drawContours(thresh, contours, -1, (0, 255, 0), 3)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    cv2.drawContours(roi, contours, -1, (0, 255, 0), 3)
  

    # Getting convex hull
    if len(contours) > 0:
        hull = cv2.convexHull(contours[0], returnPoints=False)
        cv2.drawContours(roi, [hull], 0, (255, 0, 0), 3)

        

    cv2.imshow("ROI", roi)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("FG_Mask", fg_mask)

    keyboard = cv2.waitKey(1)
    if keyboard & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()



    