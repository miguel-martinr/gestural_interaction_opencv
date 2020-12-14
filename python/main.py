import numpy as np
import cv2 as cv

cap = cv.VideoCapture(1)

if not cap.isOpened():
    print('Unable to open cam')
    exit(0)

up_left = (350, 150)
down_right = (550, 350)


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
    cv.imshow('Roi', roi)

    keyboard = cv.waitKey(1)
    if keyboard & 0xFF == ord('q'):
        break

cap.release()

cv.destroyAllWindows()



    