import serial
import time
from rover_common import aiolcm
from rover_msgs import AMG

lcm_ = aiolcm.AsyncLCM()

def main():
	serialPort = serial.Serial("/dev/ttyS0")
	serialPort.baudrate = 115200

	while (True):
		c = serialPort.read()
		if(c == '$'):
			amgMsg = AMG()
			amgMsg.accel_x = float(serialPort.read_until(',')[:-1])
			amgMsg.accel_y = float(serialPort.read_until(',')[:-1])
			amgMsg.accel_z = float(serialPort.read_until(',')[:-1])
			amgMsg.mag_x = float(serialPort.read_until(',')[:-1])
			amgMsg.mag_y = float(serialPort.read_until(',')[:-1])
			amgMsg.mag_z = float(serialPort.read_until(',')[:-1])
			amgMsg.gyro_x = float(serialPort.read_until(',')[:-1])
			amgMsg.gyro_y = float(serialPort.read_until(',')[:-1])
			amgMsg.gyro_z = float(serialPort.read_until(',')[:-1])
			_lcm.publish('/amg', amgMsg.encode())
            
if __name__ == "__main__":
    main()
