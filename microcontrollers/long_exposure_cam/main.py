import serial
import time
#import Adafruit_BBIO.GPIO as GPIO
import UCAMII
def main():
    time.sleep(5)
    bob = serial.Serial() #ENTER PORTNAME HERE
    bob.baudrate = 57600

    #GPIO.setup("P8_7",GPIO.OUT)
    #GPIO.output("P8_7", GPIO.LOW)
    #time.sleep(1)
    #GPIO.output("P8_7", GPIO.HIGH)
    
    camera = UCAMII.UCAMII(bob)
    x = 0
    
    camera.takePicture()
    print("Image size: ", end='')
    print(camera.imageSize)
    print("number of packages: ", end='')
    print(camera.numberOfPackages())
    charlie = camera.getData() 
    while(charlie != 0):
        for x in range(len(charlie)):
            print("0x", end='')
            print(hex(camera.imgBuffer[x]), end=' ')
        print()
        charlie = camera.getData() 
    print("done downloading")

if __name__ == "__main__":
    main()
    





