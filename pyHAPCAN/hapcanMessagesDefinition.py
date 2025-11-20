from .hapcanMessage import HapcanMessage
    

########################## SYSTEM MESSAGES #########################
# Messages handled by the bootloader in programming mode
class HapcanMessage_EXIT_ALL_BOOTLOADER(HapcanMessage):
    _FRAME_TYPE = 0x0100

    @classmethod
    def from_bytes(cls, data: bytearray):
        # 0xAA 0x010 0x0 0x00 0x00 0xXX 0xXX 0xXX 0xXX 0xXX 0xXX 0xXX 0xXX CHKSUM 0xA5
        msg = cls()
        return msg
    
    def to_bytes(self):
        data = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        self._prepend_type(data, self._FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data


class HapcanMessage_EXIT_ONE_BOOTLOADER(HapcanMessage):
    _FRAME_TYPE = 0x0200

    def __init__(self, module, group):
        super().__init__()
        self.module = module
        self.group = group

    @classmethod
    def from_bytes(cls, data: bytearray):
        # 0xAA 0x020 0x0 MODULE GROUP 0xXX 0xXX 0xXX 0xXX 0xXX 0xXX 0xXX 0xXX CHKSUM 0xA5
        msg = cls(module=data[3], group=data[4])
        return msg
    
    def to_bytes(self):
        data = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        self._prepend_type(data, self._FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data

#TBD    ADDRESS_FRAME = 0x030
#TBD    DATA_FRAME = 0x040


########## Messages handled by the bootloader in normal mode ##########
#TBD    ENTER_PROG_MODE_REQ = 0x100
#TBD    REBOOT_REQ_GROUP = 0x101
#TBD    REBOOT_REQ_NODE = 0x102
#TBD    HW_TYPE_REQ_GROUP = 0x103
#TBD    HW_TYPE_REQ_NODE = 0x104
class HapcanMessage_HW_TYPE_REQ_NODE(HapcanMessage):
    _FRAME_TYPE = 0x1040

    @classmethod
    def from_bytes(cls, data: bytearray):
        # 0xAA 0x104 0x0 CHKSUM 0xA5
        msg = cls()
        return msg

    def to_bytes(self):
        data = bytearray(b'')
        self._prepend_type(data, self._FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data
    

class HapcanMessage_HW_TYPE_REQ_NODE_RESP(HapcanMessage):
    _FRAME_TYPE = 0x1041
    
    def __init__(self, serialNumber, hard, hVer):
        super().__init__()
        self.serialNumber = serialNumber
        self.hard = hard
        self.hVer = hVer

    @classmethod
    def from_bytes(cls, data: bytearray):
        # 0xAA 0x104 0x1 HARD1 HARD2 HVER 0xFF ID0 ID1 ID2 ID3 CHKSUM 0xA5
        sn = data[7]<<24 | data[8]<<16 | data[9]<<8 | data[10]
        msg = cls(serialNumber=sn, hard=data[3]<<8 | data[4], hVer=data[5])
        return msg

    def to_bytes(self):
        sn = [(self.serialNumber>>24)&0xFF, (self.serialNumber>>16)&0xFF, (self.serialNumber>>8)&0xFF, self.serialNumber&0xFF]
        data = bytearray([self.hard>>8 & 0xFF, self.hard & 0xFF, self.hVer, 0xFF, *sn])
        self._prepend_type(data, self._FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data
    

#TBD    FW_TYPE_REQ_GROUP = 0x105
#TBD    FW_TYPE_REQ_NODE = 0x106
class HapcanMessage_FW_TYPE_REQ_NODE(HapcanMessage):
    _FRAME_TYPE = 0x1060

    @classmethod
    def from_bytes(cls, data: bytearray):
        # 0xAA 0x106 0x0 CHKSUM 0xA5
        msg = cls()
        return msg
    
    def to_bytes(self):
        data = bytearray(b'')
        self._prepend_type(data, self._FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data



class HapcanMessage_FW_TYPE_REQ_NODE_RESP(HapcanMessage):
    _FRAME_TYPE = 0x1061
    
    def __init__(self, hard, hVer, aType, aVers, fVers, bootVer, bootRev):
        super().__init__()
        self.hard = hard
        self.hVer = hVer
        self.aType = aType
        self.aVers = aVers
        self.fVers = fVers
        self.bootVer = bootVer
        self.bootRev = bootRev

    @classmethod
    def from_bytes(cls, data: bytearray):
        # 0xAA 0x106 0x1 HARD1 HARD2 HVER ATYPE AVERS FVERS BVER1 BREV2 CHKSUM 0xA5
        msg = cls(data[3]<<8 | data[4], data[5], data[6], data[7], data[8], data[9], data[10])
        return msg

    def to_bytes(self):
        hard = [self.hard>>8 & 0xFF, self.hard & 0xFF]
        data = bytearray([*hard, self.hVer, self.aType, self.aVers, self.fVers, self.bootVer, self.bootRev])
        self._prepend_type(data, self._FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data

#TBD    SET_DEFAULTS_REQ = 0x107
#TBD    STATUS_REQ_GROUP = 0x108


########## Messages that can be handled by the functional firmware when bootloader is in normal mode ##########
#TBD    STATUS_REQ_NODE = 0x109
#TBD    CONTROL_MESSAGE = 0x10A
#TBD    SUPPLY_VOLT_REQ_GROUP = 0x10B
#TBD    SUPPLY_VOLT_REQ_NODE = 0x10C
class HapcanMessage_SUPPLY_VOLT_REQ_NODE(HapcanMessage):
    _FRAME_TYPE = 0x10C0

    @classmethod
    def from_bytes(cls, data: bytearray):
        # 0xAA 0x10C 0x0 CHKSUM 0xA5
        msg = cls()
        return msg
    
    def to_bytes(self):
        data = bytearray(b'')
        self._prepend_type(data, self._FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data
    

class HapcanMessage_SUPPLY_VOLT_REQ_NODE_RESP(HapcanMessage):
    _FRAME_TYPE = 0x10C1

    def __init__(self, rawVBus, rawVCpu):
        super().__init__()
        self.rawVBus = rawVBus
        self.rawVCpu = rawVCpu

    @classmethod
    def from_bytes(cls, data: bytearray):
        # 0xAA 0x10C 0x1 VOLBUS1 VOLBUS2 VOLCPU1 VOLCPU2 0xFF 0xFF 0xFF 0xFF CHKSUM 0xA5
        rawVBus = data[3]<<8 | data[4]
        rawVCpu = data[5]<<8 | data[6]
        msg = cls([rawVBus, rawVCpu])
        return msg
    
    def to_bytes(self):
        rawVBus = [self.rawVBus>>8 & 0xFF, self.rawVBus & 0xFF]
        rawVCpu = [self.rawVCpu>>8 & 0xFF, self.rawVCpu & 0xFF]
        data = bytearray([*rawVBus, *rawVCpu, 0xFF, 0xFF, 0xFF, 0xFF])
        self._prepend_type(data, self._FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data
    
    

#TBD    DESC_REQ_GROUP = 0x10D
#TBD    DESC_REQ_NODE = 0x10E
class HapcanMessage_DESC_REQ_NODE(HapcanMessage):
    _FRAME_TYPE = 0x10E0

    @classmethod
    def from_bytes(cls, data: bytearray):
        # 0xAA 0x10E 0x0 CHKSUM 0xA5
        msg = cls()
        return msg
    
    def to_bytes(self):
        data = bytearray(b'')
        self._prepend_type(data, self._FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data


class HapcanMessage_DESC_REQ_NODE_RESP(HapcanMessage):
    _FRAME_TYPE = 0x10E1

    def __init__(self, desc):
        super().__init__()
        if len(desc) > 8:
            raise ValueError("Description string too long")
        self.desc = desc

    @classmethod
    def from_bytes(cls, data: bytearray):
        # 0xAA 0x10E 0x1 abc0 abc1 abc2 abc3 abc4 abc5 abc6 abc7 CHKSUM 0xA5
        desc = data[3:10].decode('ascii')
        msg = cls(desc)
        return msg
    
    def to_bytes(self):
        data = self.desc.encode('ascii')
        data = bytearray(data + b'\0'*(8-len(data))) # Make data exactly 8 bytes long
        self._prepend_type(data, self._FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data

#TBD    DEVID_REQ_GROUP = 0x10F
#TBD    DEVID_REQ_NODE = 0x111
#TBD    UPTIME_REQ_GROUP = 0x112
#TBD    UPTIME_REQ_NODE = 0x113
#TBD    HEALTH_REQ_GROUP = 0x114
#TBD    HEALTH_REQ_NODE = 0x115


########## NORMAL MESSAGES (functional firmware when bootloader is in normal mode) ##########
#TBD    BUTTON_MESSAGE = 0x301
#TBD    RELAY_MESSAGE = 0x302
#TBD    IR_RECEIVER_MESSAGE = 0x303
#TBD    TEMP_SENSOR_MESSAGE = 0x304
#TBD    IR_TRANSMITTER_MESSAGE = 0x305
#TBD    DIMMER_MESSAGE = 0x306
#TBD    BLIND_CONTROLLER_MESSAGE = 0x307
#TBD    LED_CONTROLLER_MESSAGE = 0x308