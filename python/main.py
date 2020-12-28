import numpy as np
import cv2
import bg_substractor as bg_subst
import math

def angle(s,e,f):
    v1 = [s[0]-f[0],s[1]-f[1]]
    v2 = [e[0]-f[0],e[1]-f[1]]
    ang1 = math.atan2(v1[1],v1[0])
    ang2 = math.atan2(v2[1],v2[0])
    ang = ang1 - ang2
    if (ang > np.pi):
        ang -= 2*np.pi
    if (ang < -np.pi):
        ang += 2*np.pi
    return ang*180/np.pi


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
        cnt = contours[0]
        hull = cv2.convexHull(cnt, returnPoints=False)

        # cv2.drawContours(roi, [hull], 0, (255, 0, 0), 3)
        defects = cv2.convexityDefects(cnt, hull) 
        if defects is not None:
            for i in range(len(defects)):
                s,e,f,d = defects[i,0]
                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])
                depth = d/256.0
                print(depth)
                ang = angle(start,end,far)
                cv2.line(roi,start,end,[255,0,0],2)
                cv2.circle(roi,far,5,[0,0,255],-1)


          
        

   

    cv2.imshow("ROI", roi)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("FG_Mask", fg_mask)

    keyboard = cv2.waitKey(1)
    if keyboard & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()



    