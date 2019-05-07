import picamera
from datetime import datetime
from subprocess import call
from io import BytesIO

#Camera Dashcam Mode
def cameraDC(modeToggle, crashDetected):
    
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 30
    stream = picamera.PiCameraCircularIO(camera, seconds=30)
    camera.start_recording(stream, format='mp4')

    try:
        while modeToggle:
            camera.wait_recording(1)
            if (crashDetected):
                date = str(datetime.month) + str(datetime.day) + str(datetime.year) + " " + str(datetime.hour) + ":" + str(datetime.second)
                filename = '//home//pi//Design//piCam//Video//' + date + '.mp4'
                camera.wait_recording(15)
                stream.copy_to(filename)
    finally:
        camera.stop_recording()
        camera.close()

#Camera Road Trip Mode
def cameraRT(modeToggle):

    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 30
    date = date = str(datetime.now().month) + str(datetime.now().day) + str(datetime.now().year) + "_" + str(datetime.now().hour) + "_" + str(datetime.now().minute) + "_" + str(datetime.now().second)
    filename = '//home//pi//Design//piCam//Video//' + date
    camera.start_recording(filename + '.h264', format='h264')

    try:
        while not modeToggle:
            camera.wait_recording(1)
    except KeyboardInterrupt:
        camera.stop_recording()
        camera.close()
        call(["MP4Box", "-fps", str(30),"-add", filename + '.h264', filename + '.mp4'])
        call(["rm", filename + '.h264'])
        #camera.close()
    #finally:
        #camera.stop_recording()
        #camera.close()
        #call(["MP4Box", "-fps", str(30),"-add", filename + '.h264', filename + '.mp4'])
        #call(["rm", filename + '.h264'])

def GetFrameNum(camera):
    return camera.frame.index
