from copy import copy
import serial

from .hapcanMessage import HapcanMessage, HapcanMessageUART
from .hapcanDevice import HapcanDevice


class HapcanDeviceSerialInterface(HapcanDevice):

    def __init__(self, serial:serial.Serial, *args, **kwargs):
        super().__init__(*args, aType=101, bootVer=3, bootRev=4, aVers=1, fVers=1, **kwargs)
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
                self._processSerialRxFrame(self._rxBuffer)
            else:
                print("Invalid incoming serial frame: " + self._rxBuffer.hex(sep=" "))
            self._rxBuffer = bytearray()


    def _processSerialRxFrame(self, frame):
        try:
            f = HapcanMessageUART.from_bytes(frame)
        except ValueError as e:
            print(e)
            return

        ### Process System Messages coming from serial port ###
        if f.FRAME_TYPE == HapcanMessageUART.EXIT_ONE_BOOTLOADER.FRAME_TYPE:
            return
        
        elif f.FRAME_TYPE == HapcanMessageUART.HW_TYPE_REQ_NODE.FRAME_TYPE:
            self._sendSerialMessage(HapcanMessageUART.HW_TYPE_REQ_NODE_RESP(hard=self.hard, hVer=self.hVer, serialNumber=self.serialNumber))
            return

        elif f.FRAME_TYPE == HapcanMessageUART.FW_TYPE_REQ_NODE.FRAME_TYPE:
            self._sendSerialMessage(HapcanMessageUART.FW_TYPE_REQ_NODE_RESP(hard=self.hard, hVer=self.hVer, aType=self.aType, aVers=self.aVers, fVers=self.fVers, bootVer=self.bootVer, bootRev=self.bootRev))
            return

        elif f.FRAME_TYPE == HapcanMessageUART.DESC_REQ_NODE.FRAME_TYPE:
            desc0 = self.description[0:8]
            desc1 = self.description[8:16]
            self._sendSerialMessage(HapcanMessageUART.DESC_REQ_NODE_RESP(desc0))
            self._sendSerialMessage(HapcanMessageUART.DESC_REQ_NODE_RESP(desc1))
            return

        elif f.FRAME_TYPE == HapcanMessageUART.SUPPLY_VOLT_REQ_NODE.FRAME_TYPE:
            self._sendSerialMessage(HapcanMessageUART.SUPPLY_VOLT_REQ_NODE_RESP(rawVBus=self.rawVBus, rawVCpu=self.rawVCpu))
            return

        # Forward other messages to the HAPCAN network
        try:
            f = HapcanMessage.from_bytes(frame)
            f._sender = self
            self._emulator.broadcastCanMessage(f)
        except ValueError as e:
            print(e)
            return


    def _sendSerialFrame(self, data:bytearray):
        frame = copy(data)
        HapcanMessage._append_checksum(frame)
        HapcanMessage._append_header_trailer(frame)
        self.serial.write(frame)


    def _sendSerialMessage(self, message:HapcanMessage):
        m = message.to_bytes()
        self.serial.write(m)


    def processCanApplicationMessage(self, m):
        # Resend every CAN message to the serial interface
        self._sendSerialMessage(m)