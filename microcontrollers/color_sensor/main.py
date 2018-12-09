import serial
import time
from rover_common import aiolcm
from rover_msgs import color

lcm_ = aiolcm.AsyncLCM()

def main():
	serialPort = serial.Serial("/dev/ttyS0")
	serialPort.baudrate = 9600

	while (True):
		c = serialPort.read()
		if(c == '$'):
			colorMsg = color()
			colorMsg.red = int(serialPort.read_until(',')[:-1])
			colorMsg.green = int(serialPort.read_until(',')[:-1])
			colorMsg.blue = int(serialPort.read_until(',')[:-1])
			_lcm.publish('/color', colorMsg.encode())
            
if __name__ == "__main__":
    main()
