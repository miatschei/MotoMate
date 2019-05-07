# actions during roadtrip
# nick idk how the camera works im gonna need help

import serial, time, os
from datetime import datetime
from gps_parse import parse_data
from subprocess import call
from sms import sendText
import picamera

# set up serial conection


def roadtrip_handling(ser, q, event, q_crash):
    # this happens when mode is ROAD_R
    while event.isSet():
        # check for that
        if (q.queue[0] == "ROAD_R"):
            print('roadtrip triggered')
            # if in roadtrip mode
            # set up
            date = str(datetime.now().month) + str(datetime.now().day) + str(datetime.now().year) + "_" + str(datetime.now().hour) + "_" + str(datetime.now().minute) + "_" + str(datetime.now().second)
            filename = '//home//pi//Design//piCam//Video//' + 'MM' + date

            txtfile = filename + '.txt'
            f = open(txtfile, 'w+') # open txt file
            while True:
                try:
                    camera = picamera.PiCamera()
                    camera.resolution = (640, 480)
                    camera.framerate = 30
                    break
                except:
                    continue

            camera.start_recording(filename + '.h264', format='h264')
            loc_temp = None # placeholder loc variable

            while (q.queue[0] == "ROAD_R"):
                # while true
                camera.wait_recording(1)
                # set up last known location
                try:
                    loc = parse_data(ser)
                    if (loc != None):
                        loc_temp = loc # set last known location
                        f.write(loc)
                        f.write('\n')
                except:
                    pass
                # do crash handling
                if (len(q_crash.queue) != 0): # this is so we dont get weird timing errors
                    crash_event = q_crash.queue[0] # get last crash event w/o removal
                    if crash_event.isSet():
                        msg = "Last known location: " + str(loc_temp)
                        print(msg)

                        # send text
                        sendText(9319933268, "Crash detected. " + msg)
                        q_crash.queue.clear() # clear queue

            
                time.sleep(0.05)

            # when state changes
            # need to account for keyboard interrupt :0
            camera.stop_recording()
            stream = picamera.PiCameraCircularIO(camera, seconds=30)
            camera.start_recording(stream, format='h264')
            camera.close()
            call(["MP4Box", "-fps", str(30),"-add", filename + '.h264', filename + '.mp4'])
            call(["rm", filename + '.h264'])
            f.close()
            print('closed file')

        time.sleep(0.025) 
