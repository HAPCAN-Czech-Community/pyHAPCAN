from .hapcanMessage import HapcanMessageUART
    


class EXIT_ONE_BOOTLOADER(HapcanMessageUART):
    # 0xAA 0x020 0x0 0xXX 0xXX 0xXX 0xXX 0xXX 0xXX 0xXX 0xXX CHKSUM 0xA5
    FRAME_TYPE = 0x0200

    @classmethod
    def from_bytes(cls, data: bytearray):
        msg = cls()
        return msg
    
    def to_bytes(self):
        data = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00')
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data


class ADDRESS_FRAME(HapcanMessageUART):
    # 0xAA 0x030 0x0 ADRU ADRH ADRL 0xXX 0xXX CMD 0xXX 0xXX CHKSUM 0xA5
    FRAME_TYPE = 0x0300

    def __init__(self, addr, cmd, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addr = addr
        self.cmd = cmd

    @classmethod
    def from_bytes(cls, data: bytearray):
        addr = (data[3] << 16) | (data[4] << 8) | data[5]
        cmd = data[8]
        msg = cls(addr=addr, cmd=cmd)
        return msg
    
    def to_bytes(self):
        addrU = (self.addr >> 16) & 0xFF
        addrH = (self.addr >> 8) & 0xFF
        addrL = self.addr & 0xFF
        data = bytearray([addrU, addrH, addrL, 0xFF, 0xFF, self.cmd, 0xFF, 0xFF])
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data
    
    def makeResponse(self):
        return ADDRESS_FRAME_RESP(addr=self.addr, cmd=self.cmd)
    

class ADDRESS_FRAME_RESP(ADDRESS_FRAME):
    # 0xAA 0x030 0x1 echo echo echo echo echo echo echo echo CHKSUM 0xA5
    FRAME_TYPE = 0x0301
    # Methods are inherited from ADDRESS_FRAME


class DATA_FRAME(HapcanMessageUART):
    # 0xAA 0x040 0x1 DATA0 DATA1 DATA2 DATA3 DATA4 DATA5 DATA6 DATA7 CHKSUM 0xA5
    FRAME_TYPE = 0x0400

    def __init__(self, dataBytes: bytearray, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(dataBytes) != 8:
            raise ValueError("dataBytes must be exactly 8 bytes long")
        self.dataBytes = dataBytes

    @classmethod
    def from_bytes(cls, data: bytearray):
        dataBytes = data[3:11]
        msg = cls(dataBytes=dataBytes)
        return msg
    
    def to_bytes(self):
        data = bytearray(self.dataBytes)
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data
    
    def makeResponse(self):
        return DATA_FRAME_RESP(dataBytes=self.dataBytes)
    

class DATA_FRAME_RESP(DATA_FRAME):
    # 0xAA 0x040 0x1 echo echo echo echo echo echo echo echo CHKSUM 0xA5
    FRAME_TYPE = 0x0401
    # Methods are inherited from DATA_FRAME


#TBD    ERROR_FRAME = 0x0F0