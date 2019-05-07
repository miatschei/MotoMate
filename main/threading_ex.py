import threading
import time, sys

def func(event):
    
    while event.isSet():
        print("one")
        time.sleep(0.025)

def func2(event):
    while event.isSet():
        print("two")
        time.sleep(0.025)

# set event
th_event = threading.Event()
th_event.set()
th1 = threading.Thread(target=func, args=(th_event,))
th2 = threading.Thread(target=func2, args=(th_event,))
th1.daemon = True
th2.daemon = True
th1.start()
th2.start()
try:
    while True:
        time.sleep(0.025)

except KeyboardInterrupt:
    th_event.clear()
    sys.exit()
