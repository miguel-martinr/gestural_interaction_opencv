import numpy as np
import cv2

red = [0,0,255]
green = [0,255,0]
blue = [255,0,0]
black = [0,0,0]

def get_blank_layer(r = 200, c = 200):
    return np.full((r,c, 3), 255, np.uint8)


def draw_color_menu(img):
    # Red area
    cv2.rectangle(img, (0,0), (25,25), red, -1)
    # Green Area
    cv2.rectangle(img, (0,25), (25,50), green, -1)
    # Blue Area
    cv2.rectangle(img, (0,50), (25,75), blue, -1)

def get_board():
    img = get_blank_layer()
    # draw_color_menu(img)
    return img

def get_color(point, current_color):
    if 0 <= point[0] <= 25:
         if 0 <= point[1] <= 25:
            return [0,0,255]
         if 25 < point[1] <= 50:
            return [0,255,0]
         if 50 < point[1] <= 75:
            return [255,0,0]
    
    return current_color
     

# img = get_board()

# while True:

#     cv2.imshow("foo", img)
#     wait_time = 1
#     keyboard = cv2.waitKey(wait_time)
#     if keyboard & 0xFF == ord('q'):
#         break

# cv2.destroyAllWindows()  
