import cv2
import numpy as np

trackbar_def = 200
trackbar_max = 1000
learning_rate = trackbar_def / 10000
subst = cv2.createBackgroundSubtractorMOG2(detectShadows = True)
is_trackbar_launched = False
learning_rate_window_name = "Learning Rate"

def on_learning_rate_trackbar(val):
    global learning_rate
    learning_rate = val / 10000
    blank_background = np.zeros((50, 320, 3), np.uint8)
    cv2.putText(blank_background, "Learning rate : " + str(learning_rate), (5, 25), 
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
    cv2.imshow(learning_rate_window_name, blank_background)


def launch_learning_rate_trackbar():
    global learning_rate_window_name
    position = (700, 20)
    cv2.namedWindow(learning_rate_window_name, cv2.WINDOW_AUTOSIZE)
    cv2.resizeWindow(learning_rate_window_name, 1, 50)
    cv2.moveWindow(learning_rate_window_name, position[0], position[1])
    cv2.createTrackbar("Learning rate * 10000", learning_rate_window_name, 
        trackbar_def, 1000, on_learning_rate_trackbar)
    on_learning_rate_trackbar(trackbar_def)
  
# mat : px matrix
def apply(mat):
    global is_trackbar_launched
    if not is_trackbar_launched:
        launch_learning_rate_trackbar()
        is_trackbar_launched = True
    
    global learning_rate      
    return subst.apply(mat, None, learning_rate)

