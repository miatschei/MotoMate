import serial
import rpisim
from time import sleep
import RPi.GPIO as GPIO

def setupSMS():
    
    port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=2)
    writeUART(port, "ATE0")
    print(readUART(port))
    sleep(1)
    port.flush()
    port.reset_input_buffer()
    
    #Pings SMS and turns on Auto-baud
    writeUART(port, "AT")
    modRec = readUART(port)
    #print(modRec)
    
    #First number is dB signal strength
    writeUART(port, "AT+CSQ")
    print(readUART(port))
    
    #Gets SIM card number
    #writeUART(port, "AT+CCID")
    #print(readUART(port))

    #
    #writeUART(port, "AT+CBAND?")
    #print(readUART(port))

    #
    #writeUART(port, 'AT+CBAND="DCS_MODE"')
    #print(readUART(port))
    
    #Checks that you're registered to a network. Second number is 1 or 5
    writeUART(port, "AT+CREG?")
    trash = readUART(port)
    regNet = trash.split(",")[1][:1]
    #print(trash)

    #Force to connect to network
    #writeUART(port, "AT+CREG=1")
    #print(readUART(port))
    #print(readUART(port))
    
    #Get module name and revision
    #writeUART(port, "ATI")
    #print(readUART(port))
    
    #Checks that you're connected with the network
    #writeUART(port, "AT+COPS?")
    #print(readUART(port))
    
    #Returns list of network providers in area
    #writeUART(port, "AT+COPS=?")
    #print(readUART(port))
    #print(readUART(port))
    
    #Second number indicates % full of battery; Third is actual voltage in mV
    #writeUART(port, "AT+CBC")
    #print(readUART(port))
    
    return modRec, regNet, port
    
def readUART(port):
    
    sleep(0.02)
    return port.read(80).decode().strip("\r\r\n")
    
def writeUART(port, txData):

    sleep(0.2)
    txData = txData + "\r\n"
    port.write(txData.encode('utf-8'))

def sendText(cellNum, message):
    #sleepSMS(False)
    try:
        modRec, regNet, port = setupSMS()
        if modRec == "OK" and (regNet == "1" or regNet == "5"):
            print("SMS Setup Complete")
            writeUART(port, "AT+CMGF=1")
            print(readUART(port))
            writeUART(port, 'AT+CMGS="+1' + str(cellNum) + '"')
            #Logan remove if not working to debug
            print(readUART(port))
            #sends message ending with Ctrl+Z character(ASCII 26)
            writeUART(port, message + '\x1A')
            #Logan remove if not working to debug
            print(readUART(port))
            print(readUART(port))
            
            port.close()
        else:
            print("SMS Setup Failed")
            print("modRec = ", modRec)
            print("regNet =", regNet)
            port.close()
            #sleepSMS(True)
    except:
        print("Couldn't connect to the SMS Module")
    
#Will probably not want to use this function as is and just set it up with your other GPIO(remove references in above function)
def sleepSMS(goodnight = True):
    
    GPIO.setmode(GPIO.BCM)
    pinout = 27
    sleepState = goodnight
    GPIO.setup(pinout,GPIO.OUT)

#sendText(9319933268, "Test. Reply to Logan if you got this message")
