import numpy as np
import cv2 as cv
import bg_substractor as bg_subst

learning_rate = -1






cap = cv.VideoCapture("http://192.168.1.51:4747/mjpegfeed?640x480")



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

    frame = cv.flip(frame, 1)
    roi = frame[up_left[1]:down_right[1], 
        up_left[0]:down_right[0], :]

    
    cv.rectangle(frame, up_left, down_right, (255,0,0))
    cv.imshow('Frame', frame)
    
    # Substracting background
    roi = bg_subst.apply(roi)



    cv.imshow("Learning Rate", roi)

    keyboard = cv.waitKey(1)
    if keyboard & 0xFF == ord('q'):
        break



cap.release()
cv.destroyAllWindows()



    