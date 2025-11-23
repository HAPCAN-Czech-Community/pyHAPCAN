from copy import copy
import serial

from .hapcanMessage import HapcanMessage, HapcanMessageUART
from .hapcanDevice import HapcanDevice


class HapcanDeviceSerialInterface(HapcanDevice):

    def __init__(self, serial:serial.Serial, *args, **kwargs):
        super().__init__(*args, aType=101, bootVer=3, bootRev=4, aVers=0, fVers=1, **kwargs)
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
        # Check frame length to determine if it's a CAN message to be forwarded to the HAPCAN network
        if len(frame) == HapcanMessage.FRAME_LENGTH:
            try:
                f = HapcanMessage.from_bytes(frame)
                f._sender = self
                self._emulator.broadcastCanMessage(f)
            except ValueError as e:
                print(e)
            finally:
                return

        # Other frame lengths should be handled as UART system messages
        try:
            f = HapcanMessageUART.from_bytes(frame)
        except ValueError as e:
            # Should not happen, as we already checked the frame start and end
            # Unknown frame types should generate a generic HapcanMessageUART
            print(e)
            return

        ## Process programming messages
        if f.FRAME_TYPE == HapcanMessageUART.EXIT_ONE_BOOTLOADER.FRAME_TYPE:
            return
        
        #TBD    ADDRESS_FRAME = 0x030
        #TBD    DATA_FRAME = 0x040


        # Process system messages
        elif f.FRAME_TYPE == HapcanMessageUART.ENTER_PROG_MODE_REQ.FRAME_TYPE:
            self._sendSerialMessage(HapcanMessageUART.ENTER_PROG_MODE_REQ_RESP(bootVer=self.bootVer, bootRev=self.bootRev))
            return
        
        elif f.FRAME_TYPE == HapcanMessageUART.REBOOT_REQ_NODE.FRAME_TYPE:
            return
        
        elif f.FRAME_TYPE == HapcanMessageUART.HW_TYPE_REQ_NODE.FRAME_TYPE:
            self._sendSerialMessage(HapcanMessageUART.HW_TYPE_REQ_NODE_RESP(hard=self.hard, hVer=self.hVer, serialNumber=self.serialNumber))
            return

        elif f.FRAME_TYPE == HapcanMessageUART.FW_TYPE_REQ_NODE.FRAME_TYPE:
            self._sendSerialMessage(HapcanMessageUART.FW_TYPE_REQ_NODE_RESP(hard=self.hard, hVer=self.hVer, aType=self.aType, aVers=self.aVers, fVers=self.fVers, bootVer=self.bootVer, bootRev=self.bootRev))
            return
        
        elif f.FRAME_TYPE == HapcanMessageUART.SUPPLY_VOLT_REQ_NODE.FRAME_TYPE:
            self._sendSerialMessage(HapcanMessageUART.SUPPLY_VOLT_REQ_NODE_RESP(rawVBus=self.rawVBus, rawVCpu=self.rawVCpu))
            return

        elif f.FRAME_TYPE == HapcanMessageUART.DESC_REQ_NODE.FRAME_TYPE:
            desc0 = self.description[0:8]
            desc1 = self.description[8:16]
            self._sendSerialMessage(HapcanMessageUART.DESC_REQ_NODE_RESP(desc0))
            self._sendSerialMessage(HapcanMessageUART.DESC_REQ_NODE_RESP(desc1))
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