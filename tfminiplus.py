import time
import serial
import requests

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
            return
        

        for i in range(len(rx_data)):
            print(hex(rx_data[i]), end=" ")
            if i == 4 :
                print()

        rx_data = rx_data[5:]

        distance = calDistance(rx_data[2], rx_data[3])
        print()
        print("{:.1f} cm".format(distance))

        print()

    else:
        if len(rx_data) == 0:
            print("Empty Data")
        else:
            print("Invalid Response Header")
    
    ser.close()
    return
   
    
if __name__ == '__main__':
    
    for j in range(500):
        lidarstart()
        time.sleep(1)

          
    
           

       

       