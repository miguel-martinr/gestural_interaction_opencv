import cv2 as cv

learning_rate = -1
subst = cv.createBackgroundSubtractorMOG2(detectShadows = True)
is_trackbar_launched = False

def on_learning_rate_trackbar(val):
    global learning_rate 
    learning_rate = val / 10000


def launch_learning_rate_trackbar():
    window_name = "Learning Rate"
    position = (700, 20)
    cv.namedWindow(window_name, cv.WINDOW_NORMAL)
    cv.resizeWindow(window_name, 300, 30)
    cv.moveWindow(window_name, position[0], position[1])
    cv.createTrackbar("Learning rate * 10000", "Learning Rate", 200, 1000,
        on_learning_rate_trackbar)
  
# mat : px matrix
def apply(mat):
    global is_trackbar_launched
    if not is_trackbar_launched:
        launch_learning_rate_trackbar()
        is_trackbar_launched = True
    
    global learning_rate      
    return subst.apply(mat, None, learning_rate)

