#!/usr/bin/python
import serial
#from rover_common import aiolcm
#from rover_msgs import Odometry

def main():
 #   lcm = aiolcm.AsyncLCM()
	print("Hello World!")
	serialPort = serial.Serial("/dev/ttyUSB1")
	serialPort.baudrate = 4800
	serialPort.bytesize = serial.EIGHTBITS
	serialPort.parity = serial.PARITY_NONE
	serialPort.stopbits = serial.STOPBITS_ONE
    
	while (True):
		oneByte = serialPort.read()
		if (oneByte == '$'):
			fiveBytes = serialPort.read(5);
			if (fiveBytes == 'GPRMC'):
#               Odometry = Odometry()
				serialPort.read_until(',')[:-1]
				serialPort.read_until(',')[:-1]
				serialPort.read_until(',')[:-1]
				latitude = float(serialPort.read_until(',')[:-1])
				serialPort.read_until(',')[:-1]
				longitude = float(serialPort.read_until(',')[:-1])
				serialPort.read_until(',')[:-1]
				speed = float(serialPort.read_until(',')[:-1])
				bearing = float(serialPort.read_until(',')[:-1])
#				Odometry.latitude_deg = int(latitude/100)
#				Odometry.longitude_deg = int(longitude/100)
#				Odometry.latitude_min = latitude - (Odometry.latitude_deg * 100)
#				Odometry.longitude_min = longitude  - (Odometry.longitude_deg * 100)
#				Odometry.bearing_deg = bearing
#				Odometry.speed = speed
#               lcm.publish('/some channel', Odometry.encode())

if __name__ == "__main__":
    main()

