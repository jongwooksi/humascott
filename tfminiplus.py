import time
import serial
import requests
from pantilt import *

'''
  programmed by Jongwook Si
  Sensor: TF MINI-PLUS

'''

requestHeader = bytearray([0x5A, 0x05, 0x05, 0x06, 0x6A])
responseHeader = bytearray([0x5A, 0x05, 0x05, 0x06, 0x6A])
DataHeader = bytearray([0x59, 0x59])
requestLength = 100
lidarBaudrate = 115200
lidarPort = "/dev/ttyUSB0"

def modify_header(rx_data):
    loc_index = rx_data.find(responseHeader)
    
    if rx_data[loc_index:loc_index+len(responseHeader)] == responseHeader:
        return loc_index

def calDistance(high, low): 
    calD = (low<<8) & 0xff00 | high & 0x00ff
  
    return calD * 0.1

def checkHeader(inputHeader):
    if responseHeader == inputHeader:
        return True

    else:
        return False

def checkDataHeader(inputHeader):
    if DataHeader == inputHeader:
        return True

    else:
        return False

def lidarstart():
    ser = serial.Serial(lidarPort, baudrate = lidarBaudrate, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS, timeout=1)   
    ser.write(requestHeader)
    rx_data = ser.read(requestLength)
    
    start_index = modify_header(rx_data)
    rx_data = rx_data[start_index:]
    rx_data = rx_data[:14]

    if checkHeader(rx_data[:5]):
        if not checkDataHeader(rx_data[5:7]):       
            print("Invalid Data Header")
            return -1
        

        for i in range(len(rx_data)):
            print(hex(rx_data[i]), end=" ")
            if i == 4 :
                print()

        rx_data = rx_data[5:]

        distance = calDistance(rx_data[2], rx_data[3])
        print()
        

        print()

    else:
        if len(rx_data) == 0:
            print("Empty Data")
            return -1
        else:
            print("Invalid Response Header")
            return -1
    ser.close()
    return distance
   
def scan(deg):
    move(deg)
    time.sleep(0.5)
    distance = lidarstart()
    print("deg:{} {:.1f} cm".format(deg,distance))
    
    return round(distance, 1)

if __name__ == '__main__':
    #init()
    
    for j in range(1):
        init()
        
        scandata = []
        for i in range(-90,91,1):
            scandata.append(scan(i))
            
        
        
        scandata2 = []
        for i in range(90,-91,-1):
            scandata2.append(scan(i))
            
        scandata2.reverse()
        print(scandata)
        print(scandata2)

        
        end()
        
        
    
           

       

       