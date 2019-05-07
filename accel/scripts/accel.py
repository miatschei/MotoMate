# Accelerometer fun
from FaBo9Axis_MPU9250 import MPU9250
import RPi.GPIO as GPIO
import time
import sys
#Linking camera and sms files
from subprocess import call
#sys.path.insert(0, '/home/pi/Design/piCam/scripts')
sys.path.insert(0, '/home/pi/Design/sms/scripts')
sys.path.insert(0, '/home/pi/Design/gps/scripts')
#import piCam
import picamera
from datetime import datetime
from sms import sendText
import serial
from time import sleep
from gps_parse import parse_data

# led output setup
GPIO.setmode(GPIO.BCM)
LED = 17
ledState = False
GPIO.setup(LED,GPIO.OUT)

#Setup SMS sleep pin
GPIO.setmode(GPIO.BCM)
pinout = 27
sleepState = False
GPIO.setup(pinout,GPIO.OUT)

# accel setup
imu = MPU9250()

#Camera Dashcam Setup
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
stream = picamera.PiCameraCircularIO(camera, seconds=30)
camera.start_recording(stream, format='h264')

# the poo-poo             nice
try:
    
    while True:

        accel = imu.readAccel()

        #print( 'x = ', (accel['x']))

        #print( 'y = ', (accel['y']))

        print( 'z = ', (accel['z']))

        camera.wait_recording(1)
        # if crash detected

        if (accel['z'] >= 1.03):
            # get GPS data
            msg = None
            while msg == None:
                msg = parse_data()
            # @mia need to implement a function that stores last known GPS location
            
            # send text
            #sendText(9014685884, "Crash detected. Location: " + msg)#str(datetime.now()))

            date = str(datetime.now().month) + str(datetime.now().day) + str(datetime.now().year) + "_" + str(datetime.now().hour) + "_" + str(datetime.now().minute) + "_" + str(datetime.now().second)

            filename = '//home//pi//Design//piCam//Video//' + date
            camera.wait_recording(15)
            camera.stop_recording()
            stream.copy_to(filename + '.h264', seconds = 30)
            stream.clear()
            
            call(["MP4Box", "-fps", str(30),"-add", filename + '.h264', filename + '.mp4'])
            call(["rm", filename + '.h264'])
            camera.start_recording(stream, format='h264')


        time.sleep(0.05)

except KeyboardInterrupt:

    camera.stop_recording()
    camera.close()
    sys.exit()
    
