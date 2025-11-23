from .hapcanMessage import HapcanMessage
    
    

class EXIT_ALL_BOOTLOADER(HapcanMessage):
    # 0xAA 0x010 0x0 0x00 0x00 0xXX 0xXX 0xXX 0xXX 0xXX 0xXX 0xXX 0xXX CHKSUM 0xA5
    FRAME_TYPE = 0x0100

    @classmethod
    def from_bytes(cls, data: bytearray):
        msg = cls()
        return msg
    
    def to_bytes(self):
        data = bytearray(b'\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF')
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data
    
    def isFor(self, device):
        return True


class EXIT_ONE_BOOTLOADER(HapcanMessage):
    # 0xAA 0x020 0x0 MODULE GROUP 0xXX 0xXX 0xXX 0xXX 0xXX 0xXX 0xXX 0xXX CHKSUM 0xA5
    FRAME_TYPE = 0x0200

    def __init__(self, targetNode, targetGroup, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.targetNode = targetNode
        self.targetGroup = targetGroup

    @classmethod
    def from_bytes(cls, data: bytearray):
        msg = cls(targetNode=data[3], targetGroup=data[4])
        return msg
    
    def to_bytes(self):
        data = bytearray([self.targetNode, self.targetGroup]) + bytearray(b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF')
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data
    
    def isFor(self, device):
        return (self.targetGroup == device.groupId) and (self.targetNode == device.nodeId)
    

class ADDRESS_FRAME(HapcanMessage):
    # 0xAA 0x030 0x0 MODULE GROUP ADRU ADRH ADRL 0xXX 0xXX CMD 0xXX 0xXX CHKSUM 0xA5
    FRAME_TYPE = 0x0300

    def __init__(self, targetNode, targetGroup, addr, cmd, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.targetNode = targetNode
        self.targetGroup = targetGroup
        self.addr = addr
        self.cmd = cmd

    @classmethod
    def from_bytes(cls, data: bytearray):
        targetNode = data[3]
        targetGroup = data[4]
        addr = (data[5] << 16) | (data[6] << 8) | data[7]
        cmd = data[10]
        msg = cls(targetNode=targetNode, targetGroup=targetGroup, addr=addr, cmd=cmd)
        return msg

    def to_bytes(self):
        addrU = (self.addr >> 16) & 0xFF
        addrH = (self.addr >> 8) & 0xFF
        addrL = self.addr & 0xFF
        data = bytearray([self.targetNode, self.targetGroup, addrU, addrH, addrL, 0xFF, 0xFF, self.cmd, 0xFF, 0xFF, 0xFF])
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data
    
    def makeResponse(self):
        return ADDRESS_FRAME_RESP(addr=self.addr, cmd=self.cmd)
    

class ADDRESS_FRAME_RESP(ADDRESS_FRAME):
    # 0xAA 0x030 0x1 MODULE GROUP echo echo echo echo echo echo echo echo CHKSUM 0xA5
    FRAME_TYPE = 0x0301
    # Methods are inherited from ADDRESS_FRAME


class DATA_FRAME(HapcanMessage):
    # 0xAA 0x040 0x1 MODULE GROUP DATA0 DATA1 DATA2 DATA3 DATA4 DATA5 DATA6 DATA7 CHKSUM 0xA5
    FRAME_TYPE = 0x0400

    def __init__(self, targetNode, targetGroup, dataBytes, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(dataBytes) != 8:
            raise ValueError("dataBytes must be exactly 8 bytes long")
        self.targetNode = targetNode
        self.targetGroup = targetGroup
        self.dataBytes = dataBytes

    @classmethod
    def from_bytes(cls, data: bytearray):
        targetNode = data[3]
        targetGroup = data[4]
        dataBytes = data[5:13]
        msg = cls(targetNode=targetNode, targetGroup=targetGroup, dataBytes=dataBytes)
        return msg
    
    def to_bytes(self):
        data = bytearray([self.targetNode, self.targetGroup]) + bytearray(self.dataBytes)
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data
    
    def makeResponse(self):
        return DATA_FRAME_RESP(targetNode=self.targetNode, targetGroup=self.targetGroup, dataBytes=self.dataBytes)
    

class DATA_FRAME_RESP(DATA_FRAME):
    # 0xAA 0x040 0x1 MODULE GROUP DATA0 DATA1 DATA2 DATA3 DATA4 DATA5 DATA6 DATA7 CHKSUM 0xA5
    FRAME_TYPE = 0x0401
    # Methods are inherited from DATA_FRAME


#TBD    ERROR_FRAME = 0x0F0