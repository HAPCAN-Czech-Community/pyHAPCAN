from .hapcanMessage import HapcanMessageUART
    


class ENTER_PROG_MODE_REQ(HapcanMessageUART):
    # 0xAA 0x100 0x0 CHKSUM 0xA5
    FRAME_TYPE = 0x1000

    @classmethod
    def from_bytes(cls, data: bytearray):
        msg = cls()
        return msg
    
    def to_bytes(self):
        data = bytearray(b'')
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data
    

class ENTER_PROG_MODE_REQ_RESP(HapcanMessageUART):
    # 0xAA 0x100 0x1 0xFF 0xFF BVER1 BVER2 0xFF 0xFF 0xFF 0xFF CHKSUM 0xA5
    FRAME_TYPE = 0x1001

    def __init__(self, bootVer, bootRev, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bootVer = bootVer
        self.bootRev = bootRev
    
    @classmethod
    def from_bytes(cls, data: bytearray):
        msg = cls(bootVer=data[5], bootRev=data[6])
        return msg
    
    def to_bytes(self):
        data = bytearray([0xFF, 0xFF, self.bootVer, self.bootRev, 0xFF, 0xFF, 0xFF, 0xFF])
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data


class REBOOT_REQ_NODE(HapcanMessageUART):
    # 0xAA 0x102 0x0 CHKSUM 0xA5
    FRAME_TYPE = 0x1020

    @classmethod
    def from_bytes(cls, data: bytearray):
        msg = cls()
        return msg
    
    def to_bytes(self):
        data = bytearray(b'')
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data


class HW_TYPE_REQ_NODE(HapcanMessageUART):
    # 0xAA 0x104 0x0 CHKSUM 0xA5
    FRAME_TYPE = 0x1040

    @classmethod
    def from_bytes(cls, data: bytearray):
        msg = cls()
        return msg

    def to_bytes(self):
        data = bytearray(b'')
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data
    

class HW_TYPE_REQ_NODE_RESP(HapcanMessageUART):
    # 0xAA 0x104 0x1 HARD1 HARD2 HVER 0xFF ID0 ID1 ID2 ID3 CHKSUM 0xA5
    FRAME_TYPE = 0x1041
    
    def __init__(self, serialNumber, hard, hVer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serialNumber = serialNumber
        self.hard = hard
        self.hVer = hVer

    @classmethod
    def from_bytes(cls, data: bytearray):
        sn = data[7]<<24 | data[8]<<16 | data[9]<<8 | data[10]
        msg = cls(serialNumber=sn, hard=data[3]<<8 | data[4], hVer=data[5])
        return msg

    def to_bytes(self):
        sn = [(self.serialNumber>>24)&0xFF, (self.serialNumber>>16)&0xFF, (self.serialNumber>>8)&0xFF, self.serialNumber&0xFF]
        data = bytearray([self.hard>>8 & 0xFF, self.hard & 0xFF, self.hVer, 0xFF, *sn])
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data
    

class FW_TYPE_REQ_NODE(HapcanMessageUART):
    # 0xAA 0x106 0x0 CHKSUM 0xA5
    FRAME_TYPE = 0x1060

    @classmethod
    def from_bytes(cls, data: bytearray):
        msg = cls()
        return msg
    
    def to_bytes(self):
        data = bytearray(b'')
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data


class FW_TYPE_REQ_NODE_RESP(HapcanMessageUART):
    # 0xAA 0x106 0x1 HARD1 HARD2 HVER ATYPE AVERS FVERS BVER1 BREV2 CHKSUM 0xA5
    FRAME_TYPE = 0x1061
    
    def __init__(self, hard, hVer, aType, aVers, fVers, bootVer, bootRev, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hard = hard
        self.hVer = hVer
        self.aType = aType
        self.aVers = aVers
        self.fVers = fVers
        self.bootVer = bootVer
        self.bootRev = bootRev

    @classmethod
    def from_bytes(cls, data: bytearray):
        msg = cls(data[3]<<8 | data[4], data[5], data[6], data[7], data[8], data[9], data[10])
        return msg

    def to_bytes(self):
        hard = [self.hard>>8 & 0xFF, self.hard & 0xFF]
        data = bytearray([*hard, self.hVer, self.aType, self.aVers, self.fVers, self.bootVer, self.bootRev])
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data


########## Messages that can be handled by the functional firmware when bootloader is in normal mode ##########
#TBD    STATUS_REQ_NODE = 0x109
#TBD    CONTROL_MESSAGE = 0x10A
########## Messages that can be handled by the functional firmware when bootloader is in normal mode ##########


class SUPPLY_VOLT_REQ_NODE(HapcanMessageUART):
    # 0xAA 0x10C 0x0 CHKSUM 0xA5
    FRAME_TYPE = 0x10C0

    @classmethod
    def from_bytes(cls, data: bytearray):
        msg = cls()
        return msg
    
    def to_bytes(self):
        data = bytearray(b'')
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data
    

class SUPPLY_VOLT_REQ_NODE_RESP(HapcanMessageUART):
    # 0xAA 0x10C 0x1 VOLBUS1 VOLBUS2 VOLCPU1 VOLCPU2 0xFF 0xFF 0xFF 0xFF CHKSUM 0xA5
    FRAME_TYPE = 0x10C1

    def __init__(self, rawVBus, rawVCpu, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rawVBus = rawVBus
        self.rawVCpu = rawVCpu

    @classmethod
    def from_bytes(cls, data: bytearray):
        rawVBus = data[3]<<8 | data[4]
        rawVCpu = data[5]<<8 | data[6]
        msg = cls([rawVBus, rawVCpu])
        return msg
    
    def to_bytes(self):
        rawVBus = [self.rawVBus>>8 & 0xFF, self.rawVBus & 0xFF]
        rawVCpu = [self.rawVCpu>>8 & 0xFF, self.rawVCpu & 0xFF]
        data = bytearray([*rawVBus, *rawVCpu, 0xFF, 0xFF, 0xFF, 0xFF])
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data
    
    
class DESC_REQ_NODE(HapcanMessageUART):
    # 0xAA 0x10E 0x0 CHKSUM 0xA5
    FRAME_TYPE = 0x10E0

    @classmethod
    def from_bytes(cls, data: bytearray):
        msg = cls()
        return msg
    
    def to_bytes(self):
        data = bytearray(b'')
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data


class DESC_REQ_NODE_RESP(HapcanMessageUART):
    # 0xAA 0x10E 0x1 abc0 abc1 abc2 abc3 abc4 abc5 abc6 abc7 CHKSUM 0xA5
    FRAME_TYPE = 0x10E1

    def __init__(self, desc, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(desc) > 8:
            raise ValueError("Description string too long")
        self.desc = desc

    @classmethod
    def from_bytes(cls, data: bytearray):
        desc = data[3:11].decode('ascii')
        msg = cls(desc)
        return msg
    
    def to_bytes(self):
        data = self.desc.encode('ascii')
        data = bytearray(data + b'\0'*(8-len(data))) # Make data exactly 8 bytes long
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data

########## Request for the processors identification numbers written by Microchip
#TBD    DEVID_REQ_NODE = 0x111


########## Messages that can be handled by the functional firmware when bootloader is in normal mode ##########
#TBD    UPTIME_REQ_NODE = 0x113
#TBD    HEALTH_REQ_NODE = 0x115
########## Messages that can be handled by the functional firmware when bootloader is in normal mode ##########