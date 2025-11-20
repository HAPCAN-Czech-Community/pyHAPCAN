from copy import copy
import serial

from .hapcanMessage import HapcanMessage, HapcanMessageType
from .hapcanDevice import HapcanDevice


class HapcanDeviceSerialInterface(HapcanDevice):

    def __init__(self, serial:serial.Serial, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serial = serial
        self._rxBuffer = bytearray()


    def process(self):
        buf = self.serial.read_all() # Read all available bytes from Serial

        if buf:
            for b in buf:
                self._processSerialRxByte(b)


    def _processSerialRxByte(self, b:int):
        if b == 0xAA: # Frame start
            self._rxBuffer = bytearray()

        self._rxBuffer.append(b)
        
        if self._rxBuffer[-1] == 0xA5: # Frame end
            # Check if the frame is valid
            if self._rxBuffer[0] == 0xAA:
                print("Processing incoming serial frame: " + self._rxBuffer.hex(sep=" "))
                self._processSerialRxFrame(self._rxBuffer)
            else:
                print("Invalid incoming serial frame: " + self._rxBuffer.hex(sep=" "))
            self._rxBuffer = bytearray()


    def _processSerialRxFrame(self, frame):
        try:
            f = HapcanMessage.from_bytes(frame)
        except ValueError as e:
            print("    ", e)
            return
        print(f)

        ### Process System Messages coming from serial port ###
        if f.frameType == HapcanMessageType.HW_TYPE_REQ_NODE:
            #                0xAA 0x104  0x1 HARD1 HARD2  HVER  0xFF   ID0   ID1   ID2   ID3 CHKSUM 0xA5
            response = bytearray([0x10, 0x41, 0x30, 0x00, 0x03, 0xFF, 0x01, 0x23, 0x45, 0x67])
            self._sendSerialFrame(response)

        elif f.frameType == HapcanMessageType.FW_TYPE_REQ_NODE:
            #                0xAA 0x106  0x1 HARD1 HARD2  HVER ATYPE AVERS FVERS BVER1 BREV2 CHKSUM 0xA5
            response = bytearray([0x10, 0x61, 0x30, 0x00, 0x03, 0x65, 0x00, 0x01, 0x00, 0x00])
            self._sendSerialFrame(response)

        elif f.frameType == HapcanMessageType.DESC_REQ_NODE:
            #                0xAA 0x10E  0x1  abc0  abc1  abc2  abc3  abc4  abc5  abc6  abc7 CHKSUM 0xA5
            response = bytearray([0x10, 0xE1, *(map(ord, "Python E"))])
            self._sendSerialFrame(response)
            response = bytearray([0x10, 0xE1, *(map(ord, "mulator_"))])
            self._sendSerialFrame(response)
        
        elif f.frameType == HapcanMessageType.SUPPLY_VOLT_REQ_NODE:
            #                0xAA 0x10C  0x1 VOLBUS1 VOLBUS2 VOLCPU1 VOLCPU2  0xFF  0xFF  0xFF  0xFF CHKSUM 0xA5
            response = bytearray([0x10, 0xC1,   0xC4,   0xC0,   0xFF,   0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
            self._sendSerialFrame(response)


    def _sendSerialFrame(self, data:bytearray):
        frame = copy(data)
        HapcanMessage._append_checksum(frame)
        HapcanMessage._append_header_trailer(frame)
        self.serial.write(frame)


    def _sendSerialMessage(self, message:HapcanMessage):
        self._sendSerialFrame(message.to_bytes())