# Accelerometer fun
from FaBo9Axis_MPU9250 import MPU9250
import RPi.GPIO as GPIO
import time
import sys



# accel setup
imu = MPU9250()

x = []
y = []
z = []



# x axis
print "X axis output"
input("p enter")
i = 0
while (i <= 3.0):
    accel = imu.readAccel()
    x.append(accel['x'])
    y.append(accel['y'])
    z.append(accel['z'])
    time.sleep(0.02)
    i = 0.02 + i

avg_x = sum(x)/len(x)
avg_y = sum(y)/len(y)
avg_z = sum(z)/len(z)
print "x: ", avg_x
print "y: ", avg_y  
print "z: ", avg_z

# y axis
x = []
y = []
z = []
print "Y axis output"
input("p enter")
i = 0
while (i <= 3.0):
    accel = imu.readAccel()
    x.append(accel['x'])
    y.append(accel['y'])
    z.append(accel['z'])
    time.sleep(0.02)
    i = 0.02 + i

avg_x = sum(x)/len(x)
avg_y = sum(y)/len(y)
avg_z = sum(z)/len(z)
print "x: ", avg_x
print "y: ", avg_y  
print "z: ", avg_z

# z axis
x = []
y = []
z = []
print "Z axis output"
input("p enter")
i = 0
while (i <= 3.0):
    accel = imu.readAccel()
    x.append(accel['x'])
    y.append(accel['y'])
    z.append(accel['z'])
    time.sleep(0.02)
    i = 0.02 + i

avg_x = sum(x)/len(x)
avg_y = sum(y)/len(y)
avg_z = sum(z)/len(z)
print "x: ", avg_x
print "y: ", avg_y  
print "z: ", avg_z
