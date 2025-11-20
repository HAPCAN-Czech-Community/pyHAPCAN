from .hapcanMessage import HapcanMessage
    

########################## SYSTEM MESSAGES #########################
# Messages handled by the bootloader in programming mode
class HapcanMessage_EXIT_ALL_BOOTLOADER(HapcanMessage):
    _FRAME_TYPE = 0x010

    @classmethod
    def from_bytes(cls, data: bytearray):
        # 0xAA 0x010 0x0 0x00 0x00 0xXX 0xXX 0xXX 0xXX 0xXX 0xXX 0xXX 0xXX CHKSUM 0xA5
        msg = cls()
        return msg
    
    def to_bytes(self):
        data = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data


class HapcanMessage_EXIT_ONE_BOOTLOADER(HapcanMessage):
    _FRAME_TYPE = 0x020

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
        self._prepend_type(data, self.FRAME_TYPE)
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
    _FRAME_TYPE = 0x104

    @classmethod
    def from_bytes(cls, data: bytearray):
        # 0xAA 0x104 0x0 CHKSUM 0xA5
        msg = cls()
        return msg

    def to_bytes(self):
        data = bytearray(b'')
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data
    

#TBD    FW_TYPE_REQ_GROUP = 0x105
#TBD    FW_TYPE_REQ_NODE = 0x106
class HapcanMessage_FW_TYPE_REQ_NODE(HapcanMessage):
    _FRAME_TYPE = 0x106

    @classmethod
    def from_bytes(cls, data: bytearray):
        # 0xAA 0x106 0x0 CHKSUM 0xA5
        msg = cls()
        return msg
    
    def to_bytes(self):
        data = bytearray(b'')
        self._prepend_type(data, self.FRAME_TYPE)
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
    _FRAME_TYPE = 0x10C

    @classmethod
    def from_bytes(cls, data: bytearray):
        # 0xAA 0x10C 0x0 CHKSUM 0xA5
        msg = cls()
        return msg
    
    def to_bytes(self):
        data = bytearray(b'')
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data


#TBD    DESC_REQ_GROUP = 0x10D
#TBD    DESC_REQ_NODE = 0x10E
class HapcanMessage_DESC_REQ_NODE(HapcanMessage):
    _FRAME_TYPE = 0x10E

    @classmethod
    def from_bytes(cls, data: bytearray):
        # 0xAA 0x10E 0x0 CHKSUM 0xA5
        msg = cls()
        return msg
    
    def to_bytes(self):
        data = bytearray(b'')
        self._prepend_type(data, self.FRAME_TYPE)
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