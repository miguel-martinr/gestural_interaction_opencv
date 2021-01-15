import cv2
import time
import numpy as np

### Learning Rate adjustment
# Indica que ya ha pasado el tiempo de espera
ready = False

# Indica que hay que empezar el ajuste del fondo
first_time = True

# Se usa para saber el momento en el que se inicia el ajuste
instant = -1 

# Segundos de espera para el ajuste
secs_to_wait = 4.0

# Mensaje que se muestra cuando se está ajustando
adjustment_msg = "Ajustando, por favor espera..."



### Learning Rate Trackbar parameters

# Valor que tendrá el trackbar al lanzarlo
trackbar_def = 0

# Valor máximo del trackbar
trackbar_max = 1000

# Valor que tendrá el learning_rate al lanzar el trackbar
# El máximo valor que podrá tener el learning rate es 1000 / 10000 = 0.1
# Por lo que el rango para elegir será [0, 0.1]
learning_rate = trackbar_def / 10000

subst = cv2.createBackgroundSubtractorMOG2(detectShadows = True)
is_trackbar_launched = False
learning_rate_window_name = "Learning Rate"
position = (800, 100)


# Vuelve a inicializar las variables para ajustar el fondo de nuevo
def init():
    global instant
    global ready
    global first_time 
    global is_trackbar_launched
    is_trackbar_launched = False
    instant = 1
    ready = False
    first_time = True


# Función que se invoca cuando se usa el trackbar (cambia el valor del learning_rate)
def on_learning_rate_trackbar(val):
    global learning_rate
    learning_rate = val / 1000

        
    blank_background = np.zeros((50, 320, 3), np.uint8)
    cv2.putText(blank_background, "Learning rate : " + str(learning_rate), (5, 25), 
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
    cv2.imshow(learning_rate_window_name, blank_background)
    cv2.moveWindow(learning_rate_window_name, position[0], position[1])


# Lanza la ventana con el trackbar
def launch_learning_rate_trackbar():
    global learning_rate_window_name
    global position
    cv2.namedWindow(learning_rate_window_name, cv2.WINDOW_AUTOSIZE)
    cv2.resizeWindow(learning_rate_window_name, 1, 50)
    cv2.createTrackbar("Learning rate * 10000", learning_rate_window_name, 
        trackbar_def, 1000, on_learning_rate_trackbar)
       
    on_learning_rate_trackbar(trackbar_def)
  

# Empieza el ajuste (si es el caso) y retorna el resultado 
# de llamar bg_subst.apply(mat)
# mat : px matrix
def apply(mat):
    global ready
    global first_time
    global learning_rate 
    global instant
    global position

    if ready:
        global is_trackbar_launched
        if not is_trackbar_launched:
            launch_learning_rate_trackbar()
            is_trackbar_launched = True        
        
    else: # Ajustando learning rate
        if first_time:
            learning_rate = -1
            instant = time.time()
            first_time = False
        blank_background = np.full((50,320,3), 255, np.uint8)
   
        cv2.putText(blank_background, adjustment_msg + str(secs_to_wait - int(time.time() - instant)), (5, 25), 
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
        cv2.imshow(learning_rate_window_name, blank_background)
        cv2.moveWindow(learning_rate_window_name, position[0], position[1])

        if (time.time() - instant) >= secs_to_wait:
            ready = True
            cv2.destroyWindow(learning_rate_window_name)
    return subst.apply(mat, None, learning_rate)




