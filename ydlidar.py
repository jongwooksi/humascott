import time
import serial
import requests
import math
import numpy as np
import matplotlib.pyplot as plt

'''
  programmed by Jongwook Si
  Sensor: YDLIDAR 

'''

requestHeader = bytearray([0xA5, 0x60])
responseHeader = bytearray([0xA5, 0x5A, 0x05, 0x00, 0x00, 0x40, 0x81])
requestLength = 800
lidarBaudrate = 128000
lidarPort = "/dev/ttyUSB0"
mapping = [-1 for i in range(360)]

def calPacketheader(data):
    check = (data[1]<<8) & 0xff00 | (data[0]) & 0x00ff
    
    if check == 0x55AA:
        return True
    else:
        return False

def calPackagetype(data):
    if data == 0x00:
        return True
    else:
        return False

def calSamplequantity(data):
    return data

def calStartingangle(lsb, msb): # start angle, input data: FSA
    low = (lsb >> 1)
    high = msb << 7

    return (high + low)/64

def calEndangle(lsb,msb): # ending angle, input data: LSA
    low = (lsb >> 1)
    high = msb << 7

    return (high + low)/64

def calDistance(lsb, msb): # distance (mm), input data: Si(i-th sampling data)
    little_endian = (msb<<8) & 0xff00 | lsb & 0x00ff
    #print(lsb, msb, little_endian)
    return little_endian/4

def calAnglecorrection(distance):
    if distance == 0 :
        return 0

    else:
        return math.degrees(math.atan(21.8 * (155.3 - distance)/(155.3 * distance)))


def calAngleIntermediate(fsa, lsa, lsn, i,distance): # intermediate angle, input data: FSA, LSA, LSN
    
    angle = (lsa - fsa)/(lsn-1) * (i - 1) + fsa
    angle = angle + calAnglecorrection(distance) 
    return angle

def checkHeader(inputHeader):
    if responseHeader == inputHeader:
        return True

    else:
        return False

def modify_header(rx_data):
    loc_index = rx_data.find(responseHeader)

    if rx_data[loc_index:loc_index+len(responseHeader)] == responseHeader:
        return loc_index


def lidarstart():
    ser = serial.Serial(lidarPort, baudrate = lidarBaudrate, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS, timeout=12)   
    ser.write(requestHeader)
    rx_data = ser.read(requestLength)
    
    start_index = modify_header(rx_data)
    rx_data = rx_data[start_index:]

    if checkHeader(rx_data[:7]):
        if not calPacketheader(rx_data[7:9]):
            print("Invalid Packet Header")
            ser.close()
            return
        if not calPackagetype(rx_data[9]):
            print("Invalid Packet type")
            ser.close()
            return

      
        lsn = calSamplequantity(rx_data[10])
        fsa = calStartingangle(rx_data[11], rx_data[12])
        lsa = calEndangle(rx_data[13], rx_data[14])

        if lsn == 1:
            print("need to over 2 frame (LSN)")
            ser.close()
            return

        for i in range(lsn):
            num = 2*i + 17
            distance = calDistance(rx_data[num], rx_data[num+1])
            val_angle = calAngleIntermediate(fsa, lsa, lsn, i+1 ,distance)

            if int(val_angle) == 360:
                val_angle = 0

            if not distance == 0:
                mapping[int(val_angle)] = distance
                #print("i: {} distance: {:.2f} val_angle: {:.4f}".format(i+1, distance, int(val_angle)))
           
        
    else:
        print("Invalid Response Header")
    
    ser.close()
if __name__ == '__main__':
    
    while True:
        lidarstart()

        for i in range(len(mapping)):
            print("degree: {}, distance: {:.2f}".format(i, mapping[i]))

        X = np.linspace(2*np.pi,0,360)
        plt.gca(polar=True) 
        plt.scatter(X,mapping, s = 5)
        plt.xticks(rotation=-90)
        plt.savefig("./result.png")
        plt.cla()    
    
           

       

       