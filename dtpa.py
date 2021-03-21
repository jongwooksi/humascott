import serial
import requests
import time

'''
  programmed by Jongwook Si
  Sensor: DTPA-UART-3232

'''

requestHeader = bytearray([0x11, 0x00, 0x00, 0x04, 0x01, 0x98])
requestLength = 2054
dtpaBaudrate = 115200
dtpaPort = "/dev/ttyUSB0"
minRange = -10
maxRange = 200
maxIndex = 1023
minRangeSensor = -20
maxRangeSensor = 70

def is_Range(dex):
    if dex > minRange and dex < maxRange:
        return dex

    else:
        return "Out of Range"

def is_RangeSensor(dex):
    if dex > minRangeSensor and dex < maxRangeSensor:
        return dex

    else:
        return "Out of Range"

def deximal(high, low):
	dex = ((high << 8) + low)
	
	if high > 128: 
		byte_mask = ~0xFFFF
		result = ( ((high << 8) + low) | byte_mask ) >> 4
		return round(result * 0.1, 1)

	else:
		return round(dex * 0.1, 1)

def transData(rx_data, number):
	p_num = 2*number + 4

	dex = deximal(rx_data[p_num], rx_data[p_num+1])

	return is_Range(dex)

def transSensor(high, low):
	dex = deximal(high, low)
	return is_RangeSensor(dex)

def printfunction(value):
	if type(value) is float:
		print("{:.1f}".format(value))

	else:
		print("{err}".format(err=value))

def dtpaStart():	
	
	ser = serial.Serial(dtpaPort, baudrate = dtpaBaudrate, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS, timeout=1)

	ser.write(bytearray(requestHeader))
	rx_data = ser.read(requestLength)

	dtpavalue = []
	
	for i in range(maxIndex+1):
		value = transData(rx_data, i)
		dtpavalue.append(value)
		
	ser.close()
	return dtpavalue
	
if __name__ == "__main__":
    while True:
		dtpaStart()
		print(dtpavalue)


