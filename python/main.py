import numpy as np
import cv2 as cv

cap = cv.VideoCapture(1)

if not cap.isOpened():
    print('Unable to open cam')
    exit(0)

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# print ("W:", frame_width, "H:", frame_height)
fourcc = cv.VideoWriter_fourcc('M','J','P','G')
out = cv.VideoWriter('out.avi', fourcc, 20.0, 
    (frame_width, frame_height))

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame. Exiting...")
        exit(0)
    cv.imshow('Frame', frame)

    out.write(frame)

    keyboard = cv.waitKey(1)
    if keyboard & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv.destroyAllWindows()


# def record(output_file):
    