# En ejecución:
#   Presionar c para cambiar de modo:
#     Modo detect: Imprime cuantos dedos hay levantados
#    
#    
#     Modo drawing: Permite dibujar utilizando como cursor el punto medio entre dos dedos levantados.
#       Si la variable use_white_board está a True se dibuja en una imagen en blanco 
#       Si está a False se dibuja sobre la propia imagen de la cámara.
#
#       Para seleccionar el color simplemente sitúa el cursor sobre el color deseado
#       Para limpiar el lienzo presiona r

      
import numpy as np
import cv2
import bg_substractor as bg_subst
import math
import drawing

import tkinter

# Calcula el ángulo entre tres puntos (start, end y far)
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

# Devuelve el índice del contorno con mayor perímetro
def larger_contour_index_of(contours):
    if len(contours) == 0:
        return None

    larger_cnt_index = 0
    for i in range(len(contours)):
        if cv2.arcLength(contours[i], closed = True) > cv2.arcLength(contours[larger_cnt_index], closed = True):
            larger_cnt_index = i
    return larger_cnt_index


### Devuelve el número de dedos levantadas
# finger_joins : nº de uniones de dedos
# hand_bounding_rect : bounding rectangle de la mano
#   La forma de hand_bounding_rect es (X, Y, width, height)
#   donde (X,Y) es la esquina superior izquierda del mismo.
def num_of_fingers_up(finger_joins, hand_bounding_rect):
    # Error
    if finger_joins < 0:
      return -1

    hand_height = hand_bounding_rect[3]
    hand_width = hand_bounding_rect[2]
    h_w_relation = hand_height / hand_width
    # print(h_w_relation)

    if finger_joins >= 1 and h_w_relation > 1.0:
      return finger_joins + 1
    
    # Closed hand
    if finger_joins == 0 and 0.8 <= h_w_relation  <= 1.15: 
        return 0
    # One finger up (vertical)
    if finger_joins == 0 and 1.6 <= h_w_relation <= 2.4:
        return 1

    # Horizontal thumb up
    if 0.5 <= h_w_relation < 0.8:
        return 1
    

    return 0

### Identifica gesto de rock "lml"
# defect = (start, end, far, depth, ang)
def is_lml_gesture(fingers_up, defects):
    # lml
    if len(defects) == 1:
        defect = defects[0]
        if fingers_up == 2 and 90 <= defect[0][0] - defect[1][0] <= 110:
            return True
    return False

### Identifica gesto de saludo alien de cuatro dedos
# defect = (start, end, far, depth, ang)
def is_alien_salute(fingers_up, defects):
    # Four finger alien salute 
    if len(defects) == 3 and fingers_up == 4:
        count_alien_angs = 0
        i = 0
        for defect in defects:
            i += 1
            if 45 <= defect[4] <= 82:
                count_alien_angs += 1
        if count_alien_angs == 3:
            return True
    return False




##################################################################################################
show_fg_mask = True
show_roi = False

show_filtered_lines = False
show_bounding_rect = False or show_filtered_lines
show_filtered_conv_defects =  False or show_filtered_lines
show_filtered_middle_points = False or show_filtered_lines


##################################################################################################
### MODES
drawing_mode = False
gestures_mode = True

use_camera = True 
use_white_board = False
keep_running = True
mode_changed = False

##################################################################################################


# Selecting img source
if use_camera:
    # vid_src = "http://192.168.1.51:4747/mjpegfeed?640x480"
    vid_src = 1
else:
    vid_src = "test.avi"
cap = cv2.VideoCapture(vid_src)


if not cap.isOpened():
   print('Unable to open cam')
   exit(0)

bg_subst.init()


# Roi Region of interest points
up_left = (400, 100)
down_right = (600, 300)
roi_h = down_right[1] - up_left[1] 
roi_w = down_right[0] - up_left[0]


while keep_running:


    if mode_changed:
        mode_changed = False

    if drawing_mode:
        
        # Color inicial del puntero para dibujar
        cur_color = drawing.black

        # Si no se usa la pizarra, se dibujará sobre la propia imagen
        # por lo que draw_points almacenará los puntos por donde pase el cursor
        if not use_white_board:
            draw_points = []
        else:
            # En el caso contrario se dibujará sobre un lienzo blanco
            drawing_board = drawing.get_board()


    while keep_running and not mode_changed:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame. Exiting...")
            exit(0)

        if use_camera:
            frame = cv2.flip(frame, 1)

        # Seleccionamos el área de interés de la imagen capturada
        roi = frame[up_left[1]:down_right[1], 
            up_left[0]:down_right[0], :]
        
        

        
        cv2.rectangle(frame, up_left, down_right, (255,0,0))
        
        
        # Substracting background
        fg_mask = bg_subst.apply(roi)


        # Finding contours
        contours, hierarchy = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
        

        # Getting larger contour index
        cnt_index = larger_contour_index_of(contours)
        cv2.drawContours(fg_mask, contours, cnt_index, (255, 255, 255), 3)


        if drawing_mode:
            # Draws color menu
            drawing.draw_color_menu(frame, up_left)

        cv2.imshow('Frame', frame)

        # Fingers joints
        fingers_j = 0

        # Getting convex hull 
        if len(contours) > 0:
            cnt = contours[cnt_index]

            # Getting bounding rectangle
            rect = cv2.boundingRect(cnt)
            pt1 = (rect[0],rect[1])
            pt2 = (rect[0]+rect[2],rect[1]+rect[3])
        
            
            if show_bounding_rect:
                cv2.rectangle(roi,pt1,pt2,(0,0,255),3)

            hull = cv2.convexHull(cnt, returnPoints=False)
            # make hull index monotonous
            hull.sort(0)

            # Getting convexity defects
            defects = cv2.convexityDefects(cnt, hull) 

            if defects is not None:
                filtered_defects = []
                for i in range(len(defects)):
                    s,e,f,d = defects[i,0]
                    start = tuple(cnt[s][0])
                    end = tuple(cnt[e][0])
                    far = tuple(cnt[f][0])
                    depth = d/256.0
                    ang = angle(start,end,far)
                    
                    # Filtering defects
                    # La relación entre la distancia de far a la malla y la altura del rect
                    # permite filtrar los defectos entre los dedos.
                    depth_heigh_rel = depth / rect[3]
                    
                    
                    if ang < 90 and 0.25 < depth_heigh_rel < 0.8: # Lo aumenté de 0.5 a 0.8 para permitir dibujar mejor
                        fingers_j += 1
                        # print(ang)
                        filtered_defects.append((start,end,far,depth, ang))
                        middle_point = (int((end[0] - start[0])/2) + start[0], int((end[1] - start[1])/2) + start[1])
                        if show_filtered_middle_points:
                            # Dibuja la línea recta entre f y el punto medio 
                            # entre start y end
                            cv2.line(roi, far, middle_point, [0,255,0],2)


                        if show_filtered_conv_defects:
                            # Muestra defectos de convexidad filtrados
                            cv2.line(roi,start,end,[255,0,0],2)
                            cv2.circle(roi,far,5,[0,0,255],-1)
                    
                    # Filtramos pequeños defectos ocasionados por sombras
                    if rect[3] / roi_h < 0.2:
                        fingers_up = 0
                    else:
                        fingers_up = num_of_fingers_up(fingers_j, rect)
                    
                    # Gestures mode
                    if gestures_mode:
                        if is_lml_gesture(fingers_up, filtered_defects):
                            print("ROCK")
                        elif is_alien_salute(fingers_up, filtered_defects):
                            print("ALIEN HELLO")


                    if not drawing_mode:
                        # Imprime cuantos dedos levantados hay
                        data_win_name = "Datos"
                        blank_background = np.ones((50, 320, 3), np.float)
                        cv2.namedWindow(data_win_name, cv2.WINDOW_AUTOSIZE)
                        cv2.putText(blank_background, "Dedos levantados: " + str(fingers_up), (5,25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
                        cv2.imshow(data_win_name, blank_background)
                        cv2.moveWindow(data_win_name, 800, 200)
                    else:
                        if fingers_j == 1: 
                            # Selecting color
                            cur_color = drawing.get_color(middle_point, cur_color)   
                            # Drawing    
                            if use_white_board:
                                cv2.circle(frame, (up_left[0] + middle_point[0], up_left[1] + middle_point[1]), 3, drawing.purple, -1)                 
                                cv2.circle(drawing_board, middle_point, 3, cur_color, -1)
                                cv2.imshow("Whiteboard", drawing_board)
                                cv2.moveWindow("Whiteboard", 800, 300)
                            else:
                                point = (up_left[0] + middle_point[0], up_left[1] + middle_point[1])
                                if 0 <= middle_point[0] <= 25 and 0 <= middle_point[1] <= 75:
                                    cv2.circle(frame, point, 3, drawing.purple, -1)  
                                else:
                                    draw_points.append((point, cur_color))
        if drawing_mode and not use_white_board:
            for point in draw_points:
                point_coord = point[0]
                point_color = point[1]
                cv2.circle(frame, point_coord, 3, point_color, -1)


        if show_roi:      
            cv2.imshow("ROI", roi)
            cv2.moveWindow("ROI", 100, 200)

        if show_fg_mask:
            cv2.imshow("FG_Mask", fg_mask)
            cv2.moveWindow("FG_Mask", 100, 450)
        
        if drawing_mode and not use_white_board: 
            cv2.imshow('Frame', frame)


        if use_camera:
            wait_time = 1
        else:
            wait_time = 25

        keyboard = cv2.waitKey(wait_time)
        # Stop execution
        if keyboard & 0xFF == ord('q'):
            keep_running = False
        
        # Reset whiteboard
        if drawing_mode and keyboard & 0xFF == ord('r'):
            if not use_white_board:
                draw_points = []
            else:
                drawing_board = drawing.get_board()
                cv2.imshow("Whiteboard", drawing_board)

        # Change mode
        if keyboard & 0xFF == ord('c'):
            mode_changed = True
            if drawing_mode:
                drawing_mode = False
            else:
                drawing_mode = True
                
        



    cv2.destroyAllWindows()



cap.release()
    