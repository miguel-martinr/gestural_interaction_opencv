import numpy as np
import cv2 as cv

cap = cv.VideoCapture(1)

if not cap.isOpened():
    print('Unable to open cam')
    exit(0)



while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame. Exiting...")
        exit(0)

    frame = cv.flip(frame, 1)
    cv.imshow('Frame', frame)


    keyboard = cv.waitKey(1)
    if keyboard & 0xFF == ord('q'):
        break

cap.release()

cv.destroyAllWindows()



    