#!/usr/bin/python
import serial
#from rover_common import aiolcm
#from rover_msgs import GPSOdometry

def main():
 #   lcm = aiolcm.AsyncLCM()
    print("Hello World!")
    serialPort = serial.Serial("/dev/ttyUSB0")
    serialPort.baudrate = 4800
    serialPort.bytesize = serial.EIGHTBITS
    serialPort.parity = serial.PARITY_NONE
    serialPort.stopbits = serial.STOPBITS_ONE
    
    #serialPort.open()
    #print(serialPort.write("$PGRMI,4229.34651,N,8371.11319.W,041118,180342.9,R\r\n".encode()))
    #print(serialPort.write(bytearray.fromhex('100A022600CE1003')))
    #print(serialPort.write('$PGRMC1,,1,,,,,,,,,,,,\r\n'.encode()))
#    print(serialPort.write(b'$PGRMO,,2\r\n'))
#    print(serialPort.write(b'$PGRMC1,,1,,,,,,,,,,,,,\r\n'))
    while (True):
        #print("Entering Loop")
        oneByte = serialPort.read()
        print(oneByte),
        if (oneByte == '$'):
            print("Test1")
            fiveBytes = serialPort.read(5);
            if (fiveBytes == 'GPRMC'):
#               gpsOdometry = GPSOdometry()
#               gpsOdometry.lattitude = float(moreBytes[12:22])
#               gpsOdometry.longitude = float(moreBytes[25:36])
#               gpsOdometry.speed = float(moreBytes[39:45])
#               gpsOdometry.bearing = float(moreBytes[46:51])
#               lcm.publish('/some channel', gpsOdometry.encode())
				serialPort.read_until(',')[:-1]
				serialPort.read_until(',')[:-1]
				serialPort.read_until(',')[:-1]
				lattitude = serialPort.read_until(',')[:-1]
				serialPort.read_until(',')[:-1]
				longitude = serialPort.read_until(',')[:-1]
				print("Lattitude " + lattitude)
				print("Longtitude " + longitude)

if __name__ == "__main__":
    main()

