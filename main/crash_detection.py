# CRASH DETECTION FUNCTION!!!

import time, sys, queue
import threading
from FaBo9Axis_MPU9250 import MPU9250
import RPi.GPIO as GPIO
# we'll figure out what we need l8er
from subprocess import call
sys.path.insert(0, '/home/pi/Design/sms/scripts')
#sys.path.insert(0, '/home/pi/Design/gps/scripts')
import picamera
from datetime import datetime
from sms import sendText
import serial
from time import sleep
from gps_parse import parse_data


# accel setup
imu = MPU9250()





# function: crash detection
# inputs:   end_event       threading event for ending
#           crash_event     threading event for crash

def crash_detection(end_event, crash_event, q):
    # this sets flag
    while end_event.isSet():
        th = 1.5
        accel = imu.readAccel()
        if (accel['x'] >= th or accel['y'] >= th or accel['z'] >= th):
            if (len(q.queue) == 0):
                # if no previous event set
                crash_event.set()
                q.put(crash_event)
        
        time.sleep(0.025)

def dashcam_handling(end_event, q_crash, q_mode, ser):

    while end_event.isSet():
        if (q_mode.queue[0] == "DASH_R"):

            while True:
                try:
                    #Camera Dashcam Setup (default)
                    camera = picamera.PiCamera()
                    camera.resolution = (640, 480)
                    camera.framerate = 30
                    stream = picamera.PiCameraCircularIO(camera, seconds=30)
                    camera.start_recording(stream, format='h264')
                    break
                except:
                    continue
            
            loc_temp = None # placeholder loc variable
            while(q_mode.queue[0] == "DASH_R"):

                camera.wait_recording(1)
                # set up last known location
                try:
                    loc = parse_data(ser)
                    if (loc != None):
                        loc_temp = loc # set last known location
                except:
                    pass
                if (len(q_crash.queue) != 0): # this is so we dont get weird timing errors
                    crash_event = q_crash.queue[0] # get last crash event w/o removal
                    if crash_event.isSet():
                        # get GPS data
                        msg = "Last known location: " + str(loc_temp)
                        print(msg)

                        # send text
                        sendText(9319933268, "Crash detected. Location: " + msg)
                        
                        date = str(datetime.now().month) + str(datetime.now().day) + str(datetime.now().year) + "_" + str(datetime.now().hour) + "_" + str(datetime.now().minute) + "_" + str(datetime.now().second)
                        filename = '//home//pi//Design//piCam//Video//' + 'MM' + date
                        camera.wait_recording(15)
                        camera.stop_recording()
                        stream.copy_to(filename + '.h264', seconds = 30)
                        stream.clear()
                    
                        call(["MP4Box", "-fps", str(30),"-add", filename + '.h264', filename + '.mp4'])
                        call(["rm", filename + '.h264'])
                        camera.start_recording(stream, format='h264')
                            
                            
                        q_crash.queue.clear() # clear queue
            camera.stop_recording()
            camera.close()

            time.sleep(0.05)


