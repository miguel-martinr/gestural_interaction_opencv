import numpy as np
import cv2
import bg_substractor as bg_subst
import fingers_up as fings_up
import math
import drawing

import tkinter

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

def larger_contour_index_of(contours):
    if len(contours) == 0:
        return None

    larger_cnt_index = 0
    for i in range(len(contours)):
        if cv2.arcLength(contours[i], closed = True) > cv2.arcLength(contours[larger_cnt_index], closed = True):
            larger_cnt_index = i
    return larger_cnt_index


##################################################################################################
show_filtered_lines = True
show_bounding_rect = False or show_filtered_lines
show_filtered_conv_defects =  False or show_filtered_lines
show_filtered_middle_points = False or show_filtered_lines


show_fg_mask = True
##################################################################################################
use_camera = True
drawing_mode = True

##################################################################################################


if use_camera:
    vid_src = "http://192.168.1.51:4747/mjpegfeed?640x480"
else:
    vid_src = "test.avi"

cap = cv2.VideoCapture(vid_src)



if not cap.isOpened():
    print('Unable to open cam')
    exit(0)


# Roi
up_left = (400, 100)
down_right = (600, 300)

# Drawing layer
# def get_blank_layer(r = 200, c = 200):
#     return np.full((200,200, 3), 255, np.uint8)

drawing_board = drawing.get_board()
cur_color = drawing.black


while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame. Exiting...")
        exit(0)

    if use_camera:
        frame = cv2.flip(frame, 1)

    roi = frame[up_left[1]:down_right[1], 
        up_left[0]:down_right[0], :]
    


    
    cv2.rectangle(frame, up_left, down_right, (255,0,0))
    cv2.imshow('Frame', frame)
    
    # Substracting background
    fg_mask = bg_subst.apply(roi)


    # Finding contours
    contours, hierarchy = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    

    # Getting larger contour index
    cnt_index = larger_contour_index_of(contours)
    cv2.drawContours(fg_mask, contours, cnt_index, (255, 255, 255), 3)

    # Fingers joints
    fingers_j = 0

    # Getting convex hull 
    if len(contours) > 0:
        cnt = contours[cnt_index]

        # Getting bounding rectangle
        rect = cv2.boundingRect(cnt)
        pt1 = (rect[0],rect[1])
        pt2 = (rect[0]+rect[2],rect[1]+rect[3])
        # print ("Altura: " + str(rect[3]))
        
        if show_bounding_rect:
            cv2.rectangle(roi,pt1,pt2,(0,0,255),3)

        hull = cv2.convexHull(cnt, returnPoints=False)
        # make hull index monotonous
        hull.sort(0)

        # Getting convexity defects
        defects = cv2.convexityDefects(cnt, hull) 
        if defects is not None:
            for i in range(len(defects)):
                s,e,f,d = defects[i,0]
                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])
                depth = d/256.0
                # print(depth)
                ang = angle(start,end,far)
                
                # Filtering defects
                # La relación entre la distancia de far a la malla y la altura del rect
                # permite filtrar los defectos entre los dedos.
                depth_heigh_rel = depth / rect[3]
             
                if ang < 90 and 0.25 < depth_heigh_rel < 0.5:
                    fingers_j += 1
                    
                    middle_point = (int((end[0] - start[0])/2) + start[0], int((end[1] - start[1])/2) + start[1])
                    if show_filtered_middle_points:
                        # Dibuja la línea recta entre f y el punto medio 
                        # entre start y end
                        cv2.line(roi, far, middle_point, [0,255,0],2)


                    if show_filtered_conv_defects:
                        # Muestra defectos de convexidad filtrados
                        cv2.line(roi,start,end,[255,0,0],2)
                        cv2.circle(roi,far,5,[0,0,255],-1)
                
                # Imprime cuantos dedos levantados hay
                blank_background = np.ones((50, 320, 3), np.float)
                cv2.namedWindow("Datos", cv2.WINDOW_AUTOSIZE)
                fingers_up = fings_up.calc(fingers_j, rect)
                cv2.putText(blank_background, "Dedos levantados: " + str(fingers_up), (5,25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
                cv2.imshow("Datos", blank_background)

                if drawing_mode:

                    drawing.draw_color_menu(roi)
                    # Drawing
                    if fingers_up == 2: 
                        # Selecting color
                        new_color = drawing.get_color(middle_point, cur_color)                        
                        if new_color != cur_color:
                            cur_color = new_color
                        cv2.circle(drawing_board, middle_point, 3, cur_color, -1)
                        cv2.imshow("Whiteboard", drawing_board)
                        cv2.moveWindow("Whiteboard", 700, 175)


          
        

   

    cv2.imshow("ROI", roi)
    cv2.moveWindow("ROI", 100, 200)

    if show_fg_mask:
        cv2.imshow("FG_Mask", fg_mask)
        cv2.moveWindow("FG_Mask", 100, 450)
    
    if use_camera:
        wait_time = 1
    else:
        wait_time = 25

    keyboard = cv2.waitKey(wait_time)
    if keyboard & 0xFF == ord('q'):
        break
    if keyboard & 0xFF == ord('r'):
        print("reset")
        drawing_board = drawing.get_board()
        cv2.imshow("Whiteboard", drawing_board)





cap.release()
cv2.destroyAllWindows()



    