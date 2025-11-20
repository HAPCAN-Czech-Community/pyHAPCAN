# This script emulates a HAPCAN network interfaced to Hapcan Programmer over a serial connection
# On Windows, use the com0com driver to make a connection between the emulator and the Hapcan Programmer

import serial

from pyHAPCAN import HapcanEmulator, HapcanDeviceSerialInterface


SERIAL_PORT = "COM9"



if __name__ == "__main__":

    # Create a Serial connection with the Hapcan Programmer for the Serial Interface Device
    serial = serial.Serial(port=SERIAL_PORT, baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)

    hapcan = HapcanEmulator()
    hapcan.addDevice(HapcanDeviceSerialInterface(serial, nodeId=1, groupId=1, serialNumber=0x01234567, description="Hapcan Emulator"))
    
    hapcan.processLoop()