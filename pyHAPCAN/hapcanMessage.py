

# Base class for all HAPCAN messages
class HapcanMessage:

    _message_type_subclasses = {}
    FRAME_TYPE = None


    def __init__(self, sender=None):
        self._sender = sender


    def __init_subclass__(cls, **kwargs):
        """
        Automatically called when a subclass of HapcanMessage is created.
        Used to register subclasses and their FRAME_TYPE values.
        """

        # Skip the base class itself
        if cls.__name__.startswith("HapcanMessage"):
            return
        

        # Register subclasses declaring FRAME_TYPE
        if hasattr(cls, "FRAME_TYPE"):
            baseCls = cls.__bases__[0]
            ft = cls.FRAME_TYPE

            # Store subclass in dispatch table
            baseCls._message_type_subclasses[ft] = cls

            # Make the subclass a parameter of the base class
            setattr(baseCls, cls.__name__, cls)
        
        else:
            raise ValueError(f"Subclass {cls.__name__} must define a FRAME_TYPE class attribute.")


    def to_bytes(self):
        # If this is NOT an instance of HapcanMessage itself, complain
        if type(self) is not HapcanMessage:
            raise NotImplementedError(f"{self.__class__.__name__} must implement to_bytes()")
        else:
            return self._rawFrame


    def __str__(self):
        s = self.__class__.__name__.removeprefix("HapcanMessage_") + f": \r\n"
        # Move 'checksumValid' to first position if it exists
        items = list(self.__dict__.items())
        items.sort(key=lambda kv: 0 if kv[0] == "checksumValid" else 1)
        for k, v in items:
            if k.startswith("_"): continue
            s += f"    {k}: {v}\r\n"
        return s


    @classmethod
    def from_bytes(cls, data: bytearray):
        # If this class is NOT HapcanMessage but a subclass,
        # and it did not override from_bytes, then complain
        if cls is not HapcanMessage:
            # method was not overridden if cls.from_bytes is exactly this function
            if cls.from_bytes is HapcanMessage.from_bytes:
                raise NotImplementedError(
                    f"{cls.__name__} must implement from_bytes()"
                )

        # Check if the frame starts and ends with correct bytes
        if data[0] != 0xAA or data[-1] != 0xA5:
            raise ValueError("Invalid frame")
        
        frameType = cls._extract_FRAME_TYPE(data)
        try:
            subclass = cls._message_type_subclasses[frameType]
            msg = subclass.from_bytes(data)
        except KeyError:
            # Frame type not registered, use base class
            subclass = cls
            msg = subclass()
        msg._rawFrame = data
        msg.checksumValid = cls._verify_checksum(data)
        return msg


    # To be used when the message type should be different from defined ones
    @classmethod
    def raw_from_bytes(cls, data: bytearray):
        msg = cls()
        msg._rawFrame = data
        msg.checksumValid = cls._verify_checksum(data)
        return msg


    @staticmethod
    def _extract_FRAME_TYPE(data: bytearray) -> int:
        return (data[1] << 8 | data[2])
    

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
        hi = (frameType >> 8) & 0xFF
        lo = (frameType & 0xFF)

        data.insert(0, lo)
        data.insert(0, hi)
        return data


class HapcanMessageUART(HapcanMessage):
    # Base class for UART messages
    _message_type_subclasses = {} # Separate dispatch table