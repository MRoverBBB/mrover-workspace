import time

class UCAMII:
    
    def __init__(self, input):
        self.UCAMII_BUF_SIZE = 24
        self._SYNC_COMMAND = [0xAA, 0x0D, 0x00, 0x00, 0x00, 0x00]
        self._SYNC_ACK_REPLY = [0xAA, 0x0E, 0x0D, 0x00, 0x00, 0x00]
        self._SYNC_ACK_REPLY_EXT = [0xAA, 0x0D, 0x00, 0x00, 0x00, 0x00]
        self._SYNC_FINAL_COMMAND = [0xAA, 0x0E, 0x00, 0x00, 0xF5, 0x00]
        self._INITIAL_COMMAND = [0xAA, 0x01, 0x00, 0x07, 0x09, 0x07]
        self._GENERIC_ACK_REPLY = [0xAA, 0x0E, 0x00, 0x00, 0x00, 0x00]
        self._PACK_SIZE = [0xAA, 0x06, 0x08, self.UCAMII_BUF_SIZE + 6, 0x00, 0x00]
        self._SNAPSHOT = [0xAA, 0x05, 0x00, 0x00, 0x00, 0x00]
        self._GET_PICTURE = [0xAA, 0x04, 0x01, 0x00, 0x00, 0x00]
        self.bob = input
        self.imageSize = 0
        self.imgBuffer = []
        self.image_pos = 0
        self.package_no = 0
        print('Initial is starting to be sent')
        if (self.attempt_sync()):
            print('\nCam has ACKED the SYNC', end='')
            return True
        return False
    
    def takePicture(self):
        if (self.send_initial()):
            if (self.set_package_size()):
                if (self.do_snapshot()):
                     if (self.get_picture()):
                         return 1
    def numberOfPackages(self):
        return self.imageSize / self.UCAMII_BUF_SIZE
 

    def getData(self):
        
        high = self.package_no >> 8
        low = self.package_no & 0xff
        my_ack = [0xAA, 0x0E, 0x00, 0x00, low, high]
        
        numBytes = 0
        
        if (self.image_pos == 0):
            return 0
        for i in range(6):
            self.bob.write(my_ack[i])
        if (self.image_pos < self.UCAMII_BUF_SIZE):
            numBytes = self.image_pos + 6;
        else:
            numBytes = self.UCAMII_BUF_SIZE + 6
        print("Remaining: ", end='')
        print(self.image_pos, end='')
        print(" Bytes per chunk: ", end='')
        print(numBytes, end='')
        for i in range(numBytes):
             while(self.bob.in_waiting() > 0):
                 byte = self.bob.read(1)
                 if (i >= 4 & i < numBytes - 2):
                     print("*", end='')
                     self.imgBuffer[i - 4] = byte
                     self.image_pos -= 1
             print(self.imgBuffer[byte], end='')
             print(" ", end='')
        print()
        self.package_no += 1
        if(self.image_pos <= 0):
            my_ack[4] = 0xF0
            my_ack[5] = 0xF0
            for i in range(6):
                self.bob.write(my_ack[i])
        return numBytes - 6

    def send_initial(self):
        while (self.bob.in_waiting() > 0):
            self.bob.read();
        time.sleep(.1)
        print('Sending INITIALISE...')
        for ic in _INITIAL_COMMAND:
            self.bob.write(ic)
        time.sleep(.5)
        if (self.wait_for_bytes(_GENERIC_ACK_REPLY)):
            print('INITIALISE success')
            return 1
        print("INITIALISE fail")
        return 0

    def do_snapshot(self):
        ack = [0xAA,0x0E,0x05,0x00,0x00,0x00]
        time.sleep(.1)
        print('Sending snapshot...')
        for s in self._SNAPSHOT:
            self.bob.write(s)
        time.sleep(.5)
        if(self.wait_for_bytes(ack)):
            print('snapshot success')
            return 1
        print('snapshot fail')
        return 0

    def get_picture(self):
        ack = [0xAA, 0x0E, 0x04, 0x00, 0x00, 0x00]
        imageSize = 0
        I = 0
        
        time.sleep(.1)

        print('Sending get picture...') #ln
        for x in range(6):
            self.bob.write(_GET_PICTURE[x])
        time.sleep(.5)
        if(self.wait_for_bytes(ack)):
            print('picture success') #ln
            for x in range(6):
                ack[x] = 0  
                while (not self.bob.in_waiting()>0):
                    True
                ack[x] = self.bob.read() #Last 3 bytes are image syze
                print(x, end ='')
                print(' value: ', end ='')
                print(hex(ack[x])) #ln
    
            self.imageSize = 0
            self.imageSize = (imageSize << 8 or ack[5] )
            self.imageSize = (imageSize << 8 or ack[4] )
            self.imageSize = (imageSize << 8 or ack[3] )

        self.image_pos = imageSize
        if (self.imageSize > 0):
            return 1
    
        print('picture fail') #ln

    def attempt_sync(self):
        attempts = 0
        cam_reply = 0
        ack_success = 0
        last_reply = 0

        while(attempts < 60 and ack_success == 0 ):
            #while (self.bob.in_waiting() > 0): #WTF
            #    True
            time.sleep(.2)
            print( 'sending SYNC...') # ln

            for x in range(6):
                self.bob.write(self._SYNC_COMMAND[x])
            if (self.wait_for_bytes(self._SYNC_ACK_REPLY)):
                if(self.wait_for_bytes(self._SYNC_ACK_REPLY_EXT)):
                    time.sleep(.05)
                    print("\r\nSending FINAL SYNC...")
                    for y in range(6):
                        self.bob.write(self._SYNC_FINAL_COMMAND[y])
                    return 1
        return 0

    def wait_for_bytes(command):
        j = 0
        found_bytes = 0
        received = 0
        print('\r\nWAIT: ')
        for i in command:
            print('0x', end='')
            print(hex(i), end='')
            print(' ',end='')
        print('\r\nGOT : ');
        while (self.bob.in_waiting() > 0):
            cam_reply = self.bob.read()
            if(j < 6):
                 if(( cam_reply == command[j]) or command[j] == 0x00):
                     found_bytes += 1
                     j += 1
            print('0x',end='')
            print(hex(cam_reply),end='')
            print(' ',end='')
            received += 1
            if(found_bytes == 6):
                return True
            return False
