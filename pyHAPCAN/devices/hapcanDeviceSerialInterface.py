from copy import copy
import serial
import time

from ..hapcanMessage import HapcanMessage, HapcanMessageUART
from ..hapcanDevice import HapcanDevice


def micros():
    return int(time.perf_counter() * 1_000_000)


class HapcanDeviceSerialInterface(HapcanDevice):

    def __init__(self, serial:serial.Serial, *args, **kwargs):
        super().__init__(*args, aType=101, bootVer=3, bootRev=4, aVers=0, fVers=1, **kwargs)
        self.serial = serial
        self._rxBuffer = bytearray()
        self._last_serial_rx_time = 0


    def process(self):
        buf = self.serial.read_all() # Read all available bytes from Serial

        if buf:
            for b in buf:
                self._last_serial_rx_time = micros()
                self._processSerialRxByte(b)

        if micros() >= self._last_serial_rx_time + 100: # 100 us timeout for frame end
            self._last_serial_rx_time = micros()
            self._processSerialRxByte(None) # Trigger frame end processing



    def _processSerialRxByte(self, b:int):
        # If b is None, it indicates a timeout for frame end
        if b is None:
            # Check if the frame structure is valid
            if len(self._rxBuffer) > 0:
                if self._rxBuffer[-1] == 0xA5 and self._rxBuffer[0] == 0xAA:
                    self._processSerialRxFrame(self._rxBuffer)
                    self._rxBuffer = bytearray()
                else:
                    print("Received invalid serial frame: " + self._rxBuffer.hex(sep=" "))
                    self._rxBuffer = bytearray()

        else:
            self._rxBuffer.append(b)


    def _processSerialRxFrame(self, frame):
        # Check frame length to determine if it's a CAN message to be forwarded to the HAPCAN network
        if len(frame) == HapcanMessage.FRAME_LENGTH:
            try:
                f = HapcanMessage.from_bytes(frame)
                f._sender = self
                if not f.checksumValid:
                    return False
            except ValueError as e:
                print(e)
                return False
            self._emulator.broadcastCanMessage(f)
            return True
        

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
        
        elif f.FRAME_TYPE == HapcanMessageUART.ADDRESS_FRAME.FRAME_TYPE:
            self._mem_addr = f.addr
            self._mem_cmd = f.cmd
            resp = f.makeResponse()
            self._sendSerialMessage(resp)
            return
        
        elif f.FRAME_TYPE == HapcanMessageUART.DATA_FRAME.FRAME_TYPE:
            mem = self._get_memory_by_address(self._mem_addr)

            if self._mem_cmd == mem.OPERATION.READ:
                dataBytes = mem.read(self._mem_addr, 8)
                resp = HapcanMessageUART.DATA_FRAME_RESP(dataBytes=dataBytes)

            elif self._mem_cmd == mem.OPERATION.WRITE:
                # Need to prepare response before writing to memrory, in case the nodeId/groupId changes
                resp = HapcanMessageUART.DATA_FRAME_RESP(dataBytes=bytearray(8*[0]))
                mem.write(self._mem_addr, f.dataBytes)
                dataBytes = mem.read(self._mem_addr, 8)
                resp.dataBytes = dataBytes
                
            elif self._mem_cmd == mem.OPERATION.ERASE:
                mem.erase_page(self._mem_addr)
                dataBytes = mem.read(self._mem_addr, 8)
                resp = HapcanMessageUART.DATA_FRAME_RESP(dataBytes=dataBytes)

            self._sendSerialMessage(resp)
            return


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


    def _sendSerialMessage(self, message:HapcanMessage):
        m = message.to_bytes()
        self.serial.write(m)


    def processCanApplicationMessage(self, m):
        # Resend every CAN message to the serial interface
        self._sendSerialMessage(m)