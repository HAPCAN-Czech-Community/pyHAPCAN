# This script emulates the Hapcan Serial Interface module
# On Windows, use the com0com driver to make a connection between the emulator and the Hapcan Programmer

# TODO:
#   Fix response values to something more meaningful
#   Response to the following messages from Hapcan Programmer:
#           aa 10 00 10 a5

import serial
import time
from copy import copy

from hapcanMessage import HapcanMessage, HapcanMessageType


SERIAL_PORT = "COM9"
BAUD_RATE = 115200


class HapcanEmulator(serial.Serial):

    stopFlag = False

    def __del__(self):
        self.stopFlag = True
        print("Disconnecting from " + SERIAL_PORT )
        self.close()


    def __init__(self):
        super().__init__(
            port=SERIAL_PORT,
            baudrate=BAUD_RATE,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1,
        )
        print("Connected to " + SERIAL_PORT)


    def sendFrame(self, data:bytearray):
        frame = copy(data)
        HapcanMessage._append_checksum(frame)
        HapcanMessage._append_header_trailer(frame)
        self.write(frame)


    def processLoop(self):
        buffer = bytearray()
        while not self.stopFlag:
            b = self.read() # Read a single byte

            if not b:
                continue
            if b[0] == 0xAA:
                buffer = bytearray()

            buffer.extend(b)

            if buffer[-1] == 0xA5: # Frame ending
                # Check if the frame is valid
                if buffer[0] == 0xAA:
                    print("Processing incoming frame: " + buffer.hex(sep=" "))
                    self.processFrame(buffer)
                else:
                    print("Invalid incoming frame: " + buffer.hex(sep=" "))
                buffer = bytearray()
            

    def processFrame(self, frame):
        try:
            f = HapcanMessage.from_bytes(frame)
        except ValueError as e:
            print("    ", e)
            return
        print(f)

        ### Serial interface responses ###
        if f.frameType == HapcanMessageType.HW_TYPE_REQ_NODE:
            #                0xAA 0x104  0x1 HARD1 HARD2  HVER  0xFF   ID0   ID1   ID2   ID3 CHKSUM 0xA5
            response = bytearray([0x10, 0x41, 0x30, 0x00, 0x03, 0xFF, 0x01, 0x23, 0x45, 0x67])
            self.sendFrame(response)

        elif f.frameType == HapcanMessageType.FW_TYPE_REQ_NODE:
            #                0xAA 0x106  0x1 HARD1 HARD2  HVER ATYPE AVERS FVERS BVER1 BREV2 CHKSUM 0xA5
            response = bytearray([0x10, 0x61, 0x30, 0x00, 0x03, 0x65, 0x00, 0x01, 0x03, 0x04])
            self.sendFrame(response)

        elif f.frameType == HapcanMessageType.DESC_REQ_NODE:
            #                0xAA 0x10E  0x1  abc0  abc1  abc2  abc3  abc4  abc5  abc6  abc7 CHKSUM 0xA5
            response = bytearray([0x10, 0xE1, *(map(ord, "Python E"))])
            self.sendFrame(response)
            response = bytearray([0x10, 0xE1, *(map(ord, "mulator "))])
            self.sendFrame(response)
        
        elif f.frameType == HapcanMessageType.SUPPLY_VOLT_REQ_NODE:
            #                0xAA 0x10C  0x1 VOLBUS1 VOLBUS2 VOLCPU1 VOLCPU2  0xFF  0xFF  0xFF  0xFF CHKSUM 0xA5
            response = bytearray([0x10, 0xC1,   0x00,   0x00,   0x00,   0x00, 0xFF, 0xFF, 0xFF, 0xFF])
            self.sendFrame(response)



if __name__ == "__main__":

    hapcan = HapcanEmulator()
    hapcan.processLoop()