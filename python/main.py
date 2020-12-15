import numpy as np
import cv2 as cv

learning_rate = -1

# Learning rate trackbar callback function
def on_learning_rate_trackbar(val):
    global learning_rate 
    learning_rate = val / 10000


def launch_learning_rate_trackbar():
    window_name = "Learning Rate"
    position = (700, 20)
    cv.namedWindow(window_name, cv.WINDOW_NORMAL)
    cv.resizeWindow(window_name, 300, 30)
    cv.moveWindow(window_name, position[0], position[1])
    cv.createTrackbar("Learning rate * 10000", "Learning Rate", 200, 10000,
        on_learning_rate_trackbar)
    
    




cap = cv.VideoCapture(1)
backSub = cv.createBackgroundSubtractorMOG2(detectShadows = True)


if not cap.isOpened():
    print('Unable to open cam')
    exit(0)


# Roi
up_left = (350, 150)
down_right = (550, 350)



launch_learning_rate_trackbar()

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
    roi = backSub.apply(roi, None, learning_rate)
    # print("Lr: ", learning_rate)
    cv.imshow('Roi', roi)

    keyboard = cv.waitKey(1)
    if keyboard & 0xFF == ord('q'):
        break

cap.release()

cv.destroyAllWindows()



    