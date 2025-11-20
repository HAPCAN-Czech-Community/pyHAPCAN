from abc import ABC, abstractmethod

from .hapcanUartSystemMessages import *


class HapcanDevice:

    def __init__(self, nodeId, groupId, serialNumber, aType,
                 hard=0x3000, hVer=0x03, aVers=0x00, fVers=0x00,
                 bootVer=0x00, bootRev=0x00, description="",
                 rawVBus=0x0000, rawVCpu=0x0000):
        
        # List of field names that must fit in 0–255
        byte_fields = [
            "nodeId",
            "groupId",
            "aType",
            "hVer",
            "aVers",
            "fVers",
            "bootVer",
            "bootRev"
        ]

        two_byte_fields = [
            "hard",
            "rawVBus",
            "rawVCpu"
        ]
        # Validate each byte-sized parameter
        for name in byte_fields:
            value = locals()[name]
            if not isinstance(value, int):
                raise TypeError(f"{name} must be an integer (0–255), got {type(value).__name__}")
            if not (0 <= value <= 255):
                raise ValueError(f"{name} must be in range 0–255, got {value}")

        # Validate each two-byte parameter
        for name in two_byte_fields:
            value = locals()[name]
            if not isinstance(value, int):
                raise TypeError(f"{name} must be an integer (0–65535), got {type(value).__name__}")
            if not (0 <= value <= 65535):
                raise ValueError(f"{name} must be in range 0–65535, got {value}")

        # Validate serial number
        if not isinstance(serialNumber, int):
            raise TypeError(f"serialNumber must be an integer (0x0–0xFFFFFFFF), got {type(serialNumber).__name__}")
        if not (0 <= serialNumber <= 0xFFFFFFFF):
            raise ValueError(f"serialNumber must be in range 0x0–0xFFFFFFFF, got {serialNumber}")
        
        # Validate description
        if not isinstance(description, str):
            raise TypeError(f"description must be a string, got {type(description).__name__}")
        if len(description) > 16:
            raise ValueError(f"description must be 16 characters or less, got {len(description)}")
        
        # Assign values
        self.nodeId = nodeId
        self.groupId = groupId
        self.serialNumber = serialNumber
        self.aType = aType
        self.hard = hard
        self.hVer = hVer
        self.aVers = aVers
        self.fVers = fVers
        self.bootVer = bootVer
        self.bootRev = bootRev
        self.description = description
        self.rawVBus = rawVBus
        self.rawVCpu = rawVCpu


    @abstractmethod
    def processMessage(self, m: HapcanMessage):
        # Must be handled by subclasses
        pass
    

    def process(self):
        # May be handled by subclasses which need to process something in a loop
        pass