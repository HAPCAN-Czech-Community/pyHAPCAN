from enum import Enum


class HapcanMessage:
    _message_subclasses = {}
    _FRAME_TYPE = None

    def __init__(self, response=False):
        self.response = response

    def __init_subclass__(cls, **kwargs):
        """
        Automatically called when a subclass of HapcanMessage is created.
        Used to register subclasses and their _FRAME_TYPE values.
        """
        super().__init_subclass__(**kwargs)

        # Skip the base class itself
        if cls is HapcanMessage:
            return

        # Register subclasses declaring _FRAME_TYPE
        if hasattr(cls, "_FRAME_TYPE"):
            ft = cls._FRAME_TYPE

            # Store subclass in dispatch table
            HapcanMessage._message_subclasses[ft] = cls

            # Add value dynamically to the enum if not yet present
            if ft not in HapcanMessageType.members():
                HapcanMessageType.add(cls.__name__.removeprefix("HapcanMessage_"), ft)


    @property
    def frameType(self):
        return HapcanMessageType(self._FRAME_TYPE)


    def __str__(self):
        s = str(self.frameType) + f": \r\n"
        # Move 'checksumValid' to first position if it exists
        items = list(self.__dict__.items())
        items.sort(key=lambda kv: 0 if kv[0] == "checksumValid" else 1)
        for k, v in items:
            if k.startswith("_"): continue
            s += f"    {k}: {v}\r\n"
        return s


    @staticmethod
    def from_bytes(data: bytearray):
        frameType = HapcanMessage._extract_frame_type(data)
        try:
            subclass = HapcanMessage._message_subclasses[frameType]
        except KeyError:
            # Frame type not registered, raise error
            raise ValueError("Unknown frame type: " + f"0x{frameType:03X}")
        msg = subclass.from_bytes(data)
        msg._rawFrame = data
        msg.checksumValid = HapcanMessage._verify_checksum(data)
        return msg

    @staticmethod
    def raw_from_bytes(data: bytearray):
        msg = HapcanMessage()
        msg._rawFrame = data
        msg.checksumValid = HapcanMessage._verify_checksum(data)
        return msg

    @staticmethod
    def _extract_frame_type(data: bytearray) -> int:
        return (data[1] << 8 | data[2]) >> 4
    
    @staticmethod
    def _extract_response(data: bytearray) -> bool:
        return data[2] & 0x01

    @staticmethod
    def _verify_checksum(data: bytearray):
        return sum(data[1:-2]) & 0xFF == data[-2]

    @staticmethod
    def _append_checksum(data: bytearray):
        checksum = sum(data) & 0xFF
        data.append(checksum)
        return data
    

    @staticmethod
    def _append_header_trailer(data: bytearray):
        data.insert(0, 0xAA)
        data.append(0xA5)
        return data
    

    @staticmethod
    def _prepend_type(data: bytearray, frameType: int):
        hi = (frameType >> 4) & 0xFF
        lo = (frameType & 0x0F) << 4

        data.insert(0, lo)
        data.insert(0, hi)
        return data
    
    

class HapcanMessageType:
    _members = {}

    class _Value(int):
        def __new__(cls, value, name):
            obj = int.__new__(cls, value)
            obj._name = name
            return obj

        @property
        def name(self):
            return self._name

        def __repr__(self):
            return f"<{self._name}: 0x{int(self):03X}>"
        
        def __str__(self):
            return self._name

    def __new__(cls, value):
        # lookup by numeric value
        for member in cls._members.values():
            if int(member) == value:
                return member
        member = cls.add("UNKNOWN", value)
        return member

    @classmethod
    def add(cls, name, value):
        member = cls._Value(value, name)
        cls._members[name] = member
        setattr(cls, name, member)
        return member

    @classmethod
    def members(cls):
        return dict(cls._members)


# Import all message types, needs to be at the end of the module
from hapcanUartSystemMessageTypes import *