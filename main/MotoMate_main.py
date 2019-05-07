
#  MotoMate Main
#

# THREAD LIST
# state_th  -->  thread that changes state and indication light
# detect_th -->  thread that detects crash and updates crash event
# hand_th   -->  thread that handles the actual crash activities
# road_th   -->  thread that records roadtrip data (video and gps)


# functionality
# -> crash detection // needs 2 run constantly
#   -> saves crash video //time sensitive
#   -> polls accelerometer // sep thread
# -> mode select // sep thread
# -> for road trip, do we keep recording after crash?? how does that work??

import threading, queue, sys, time
import RPi.GPIO as GPIO
from mode_select import check_state
from crash_detection import crash_detection, dashcam_handling
from roadtrip_handling import roadtrip_handling
import serial
import picamera

GPIO.setwarnings(False) # turn off gpio warnings       
        

# set up GPIO
# led output setup
GPIO.setmode(GPIO.BCM)
LED = 17
GPIO.setup(LED,GPIO.OUT)
#GPIO.output(LED, False)  

#Setup SMS sleep pin
GPIO.setmode(GPIO.BCM)
pinout = 27
sleepState = False
GPIO.setup(pinout,GPIO.OUT)

#pb setup
GPIO.setmode(GPIO.BCM)
btn = 23
GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# gps setup
port = "/dev/ttyUSB0"
ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)

# set up camera stuff here
##camera = picamera.PiCamera()
##camera.resolution = (640, 480)
##camera.framerate = 30
##stream = picamera.PiCameraCircularIO(camera, seconds=30)
##camera.start_recording(stream, format='h264')

# set up variable queues
#   accel
#   mode select

run_event = threading.Event()
run_event.set()
q_mode = queue.Queue()
e_state = "DASH_R" # default state
q_mode.put(e_state)

q_crash = queue.Queue()

# threading events
end_event = threading.Event() # designates end of main thread
end_event.set()
crash_event = threading.Event() # for crash detection

#check state thread
state_th = threading.Thread(target=check_state, args=(btn, LED, q_mode, end_event, q_crash))
state_th.start()

# detect crash thread
detect_th = threading.Thread(target=crash_detection, args=(end_event, crash_event, q_crash))
detect_th.start()

# crash handling thread
handle_th = threading.Thread(target=dashcam_handling, args=(end_event, q_crash, q_mode, ser))
handle_th.start()

# road trip handling thread
road_th = threading.Thread(target=roadtrip_handling, args=(ser, q_mode, end_event, q_crash))
road_th.start()
    
try:
    while True:
        time.sleep(0.02)
        
except KeyboardInterrupt:
    # clean up
    #camera.close()
    end_event.clear()
    GPIO.output(LED, False) 
    sys.exit()

