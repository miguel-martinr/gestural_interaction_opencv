import numpy as np
import cv2


# Colores
red = [0,0,255]
green = [0,255,0]
blue = [255,0,0]
black = [0,0,0]
purple = [128,0,128]

# Devuelve 
def get_board(height = 200, width = 200):
    return np.full((height, width, 3), 255, np.uint8)

def draw_color_menu(img, up_left = (0,0)):
    # Red area
    cv2.rectangle(img, (up_left[0], up_left[1]), (up_left[0] + 25, up_left[1] + 25), red, -1)
    # Green Area
    cv2.rectangle(img, (up_left[0], up_left[1] + 25), (up_left[0] + 25, up_left[1] + 50), green, -1)
    # Blue Area
    cv2.rectangle(img, (up_left[0], up_left[1] + 50), (up_left[0] + 25, up_left[1] + 75), blue, -1)


def get_color(point, current_color):
    if 0 <= point[0] <= 25:
        # Pointer is on red area
        if 0 <= point[1] <= 25:
            return red
        # Pointer is on green area
        if 25 < point[1] <= 50:
            return green
        # Pointer is on blue area
        if 50 < point[1] <= 75:
            return blue
    
    return current_color
     

