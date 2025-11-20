from copy import copy
import serial

from .hapcanMessage import HapcanMessage, HapcanMessageType
from .hapcanDevice import HapcanDevice

from pyHAPCAN.hapcanMessagesDefinition import *


class HapcanDeviceSerialInterface(HapcanDevice):

    def __init__(self, serial:serial.Serial, *args, **kwargs):
        super().__init__(*args, aType=101, **kwargs)
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
            self._sendSerialMessage(HapcanMessage_HW_TYPE_REQ_NODE_RESP(hard=self.hard, hVer=self.hVer, serialNumber=self.serialNumber))
        
        elif f.frameType == HapcanMessageType.FW_TYPE_REQ_NODE:
            self._sendSerialMessage(HapcanMessage_FW_TYPE_REQ_NODE_RESP(hard=self.hard, hVer=self.hVer, aType=self.aType, aVers=self.aVers, fVers=self.fVers, bootVer=self.bootVer, bootRev=self.bootRev))
        
        elif f.frameType == HapcanMessageType.DESC_REQ_NODE:
            desc0 = self.description[0:8]
            desc1 = self.description[8:16]
            self._sendSerialMessage(HapcanMessage_DESC_REQ_NODE_RESP(desc0))
            self._sendSerialMessage(HapcanMessage_DESC_REQ_NODE_RESP(desc1))
        
        elif f.frameType == HapcanMessageType.SUPPLY_VOLT_REQ_NODE:
            self._sendSerialMessage(HapcanMessage_SUPPLY_VOLT_REQ_NODE_RESP(rawVBus=self.rawVBus, rawVCpu=self.rawVCpu))


    def _sendSerialFrame(self, data:bytearray):
        frame = copy(data)
        HapcanMessage._append_checksum(frame)
        HapcanMessage._append_header_trailer(frame)
        self.serial.write(frame)


    def _sendSerialMessage(self, message:HapcanMessage):
        self.serial.write(message.to_bytes())