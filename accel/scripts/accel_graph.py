# Accelerometer fun
from FaBo9Axis_MPU9250 import MPU9250
import RPi.GPIO as GPIO
import time
import sys

# led output setup
GPIO.setmode(GPIO.BCM)
LED = 17
ledState = False
GPIO.setup(LED,GPIO.OUT)

# accel setup
imu = MPU9250()

# accel data
z_axis = []
filename = "graph_zinput.txt"
# the Shit
try:
    
    while True:

        accel = imu.readAccel()

        #print( 'x = ', (accel['x']))

        #print( 'y = ', (accel['y']))
        
        z_axis.append(accel['z'])


        time.sleep(0.02)

except KeyboardInterrupt:
    f = open(filename, "w +")
    f.write("test 1 (no input)\n")
    f.write(str(z_axis))
    f.close()
    sys.exit()
    

