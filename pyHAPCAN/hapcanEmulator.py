import time

from .hapcanMessage import HapcanMessage#, HapcanMessageType
from .hapcanDevice import HapcanDevice


class HapcanEmulator():

    def __del__(self):
        self.stopFlag = True


    def __init__(self):
        self.stopFlag = False
        self._devices = []


    def addDevice(self, device:HapcanDevice):
        self._devices.append(device)

    def createDevice(self, deviceClass, *args, **kwargs) -> HapcanDevice:
        device = deviceClass(emulator=self, *args, **kwargs)
        self.addDevice(device)
        return device

    def removeDevice(self, device:HapcanDevice):
        self._devices.remove(device)


    def broadcastCanMessage(self, message:HapcanMessage):
        for d in self._devices:
            if message._sender == d: continue # Don't send the message back to the sender
            d.processCanMessage(message)


    def processLoop(self):
        while not self.stopFlag:
            for d in self._devices:
                d.process()
            time.sleep(0.001)
            