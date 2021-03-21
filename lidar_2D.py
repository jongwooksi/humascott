import serial
import requests
import time

'''
  programmed by Jongwook Si
  Sensor: CygLIDAR D1 (2D Mode)

'''

requestHeader = bytearray([0x5A, 0x77, 0xFF, 0x02, 0x00, 0x01, 0x00, 0x03])
responseHeader = bytearray([0x5A, 0x77, 0xFF, 0xF3, 0x00, 0x01])
requestLength = 249
lidarBaudrate = 3000000
lidarPort = "/dev/ttyUSB1"
minRange = 200
maxRange = 8000

def errorCode(dex):
    if dex == 16000:
        return "Limit for valid data"
    elif dex == 16001:
        return "Low Amplitude"
    elif dex == 16002:
        return "ADC Overflow"
    elif dex == 16003:
        return "Saturation"
    elif dex == 16004:
        return "Bad Pixel"
    else:
        return "Out of Range"
        
def is_Range(dex):
    if dex > minRange and dex < maxRange:
        return True

    else:
        return False

def deximal(high, low):
    dex = ((high<<8) & 0xff00) | (low & 0x00ff)

    if is_Range(dex):
        return round(dex *0.1,1)
    else:
        return errorCode(dex)
    
	
def transData(rx_data, number):
    p_num = 2* number + 126
   
    dex = deximal(rx_data[p_num], rx_data[p_num+1])

    return dex


def checkHeader(inputHeader):
    if responseHeader == inputHeader: 
        return True

    else:
        return False

def printfunction(i, value):
    if type(value) is float:
        print("degree: {} {:.1f}cm  ".format(i,value))
    else:
        print("degree: {} {err}".format(i, err=value))

def lidarStart():
    
    ser = serial.Serial(lidarPort, baudrate = lidarBaudrate, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS, timeout=1)

    ser.write(requestHeader)
    rx_data = ser.read(requestLength)
    lidarvalue = []

    if checkHeader(rx_data[:6]):
        for i in range(-60, 61):
            value = transData(rx_data, i)

            lidarvalue.append(value)
    else:
        print("Invalid Response Header")
            
    print()
    ser.close()
    return lidarvalue
	
if __name__ == "__main__":
    while True:
        lidarStart()
        print(lidarvalue)



