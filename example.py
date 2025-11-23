# This script emulates a HAPCAN network interfaced to Hapcan Programmer over a serial connection
# On Windows, use the com0com driver to make a connection between the emulator and the Hapcan Programmer

import serial

from pyHAPCAN import HapcanEmulator, HapcanDeviceSerialInterface, HapcanDevice


SERIAL_PORT = "COM9"



if __name__ == "__main__":

    # Create a Serial connection with the Hapcan Programmer for the Serial Interface Device
    serial = serial.Serial(port=SERIAL_PORT, baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)

    hapcan = HapcanEmulator()
    hapcan.createDevice(HapcanDeviceSerialInterface, serial, nodeId=1, groupId=1, serialNumber=0x01234567, description="Hapcan Emulator")
    hapcan.createDevice(HapcanDevice, aType=0, hVer=0x03, hard=0x3000,
                        nodeId=1, groupId=1, serialNumber=0x00000201, fVers=1,
                        aVers=2, bootVer=3, bootRev=4, description="Empty test dev.")

    hapcan.processLoop()