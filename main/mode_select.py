# lets figure out pushbuttons
# and state machines

import RPi.GPIO as GPIO
import time
import sys
import picamera


# function: check_state
# inputs: e_state   current state
#         btn       push button pin
#         q         queue object

def check_state(btn, LED, q, event, q_crash):

    # "switch" statement
    # default: DASH_R
    #          DASH_P
    #          ROAD_R
    #          ROAD_P
    
    while event.isSet():
        input_state = GPIO.input(btn)
        # check if in crash
        if (len(q_crash.queue) != 0): # this is so we dont get weird timing errors
            crash_event = q_crash.queue[0] # get last crash event w/o removal
            if (crash_event.isSet() and input_state == False):
                GPIO.output(LED, True)
                time.sleep(0.025)
                GPIO.output(LED, False)
                time.sleep(0.025)
                GPIO.output(LED, True)
                time.sleep(0.025)
                GPIO.output(LED, False)
        else:
            e_state = q.queue[0] #retrieve state from queue
            if e_state == "DASH_R":
                # do dashcam mode
                # check for button
                if input_state == False: # Pressed
                    e_state = "DASH_P"
                    q.put(e_state) # put updated state to queue
                    q.get()
                    GPIO.output(LED, True)
                    # close out camera
                    #camera.stop_recording()
                    #camera.close()

        
            elif e_state == "DASH_P":
                # check for button
                if input_state == True: # Released
                    # switch 2 ROAD
                    e_state = "ROAD_R"
                    q.put(e_state) # put updated state to queue
                    q.get()


            elif e_state == "ROAD_R":
                # check for button
                if input_state == False: # Pressed
                    e_state = "ROAD_P"
                    q.put(e_state) # put updated state to queue
                    q.get()
                    GPIO.output(LED, False)
                    # close out camera
                    #camera.stop_recording()
                    #camera.close()
                    


       
            elif e_state == "ROAD_P":
                # check for button
                if input_state == True: # Released
                    # switch 2 DASH
                    e_state = "DASH_R"
                    q.put(e_state) # put updated state to queue
                    q.get()
                    # set up camera stuff here for dashcam
                    #camera = picamera.PiCamera()
                    #camera.resolution = (640, 480)
                    #camera.framerate = 30
                    

        time.sleep(0.02)
