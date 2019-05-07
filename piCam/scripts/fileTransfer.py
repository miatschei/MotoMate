from pyudev import Context, Monitor, MonitorObserver
from os import listdir, makedirs, path, system
from shutil import move, copy, copy2
from time import sleep
from subprocess import call

def transfer_video(observer, device):

        if device.action == 'add' and device.get('DEVTYPE') == 'usb_device':
            sleep(5)
            print("Type: {0}".format(device.get('DEVTYPE')))
            print("NAME: {0}".format(device.get('DEVNAME')))
            devName = device.get('DEVNAME').split("/")
            phonePath = "/run/user/1000/gvfs/mtp:host=%5Busb%3A" + devName[4] + "%2C" + devName[5] + "%5D/Phone"
            print(phonePath)
            if path.exists(phonePath):
                    if not path.exists(phonePath + "/motomatedata"):
                            makedirs(phonePath + "/motomatedata")
                    for file in listdir("/home/pi/Design/piCam/Video"):
                            system("sudo cp /home/pi/Design/piCam/Video/" + file + " " + phonePath + "/motomatedata")
                            #:
                                    #call(["rm", "/home/pi/Design/piCam/Video/" + file])
                                    #print("Whoopsie")
                                    
        

context = Context()
monitor = Monitor.from_netlink(context)

#monitor.filter_by(subsystem='bus')
observer = MonitorObserver(monitor, transfer_video)

monitor.start()
observer.start()
