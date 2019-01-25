import serial
#from rover_common import aiolcm
#from rover_msgs import GPSOdometry

def main():
 #   lcm = aiolcm.AsyncLCM()

    serialPort = serial.Serial("/dev/ttyAMA0")
    serialPort.baudrate = 19200
    serialPort.open()

    while (true):
        oneByte = serialPort.read();
        if (oneByte == '$'):
            fiveBytes = serialPort.read(5);
            if (fiveBytes == 'GPRMC'):
#               gpsOdometry = GPSOdometry()
                moreBytes = serialPort.read(51)
#               gpsOdometry.lattitude = float(moreBytes[12:22])
#               gpsOdometry.longitude = float(moreBytes[25:36])
#               gpsOdometry.speed = float(moreBytes[39:45])
#               gpsOdometry.bearing = float(moreBytes[46:51])
#               lcm.publish('/some channel', gpsOdometry.encode())
                print("Lattitude " + str(float(moreBytes[12:22])))
                print("Longtitude " + str(float(moreBytes[25:36])))
                print("Speed " + str(float(moreBytes[39:45])))
                print("Bearing " + str(float(moreBytes[46:51])))
                