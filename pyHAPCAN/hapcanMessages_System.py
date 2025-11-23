from .hapcanMessage import HapcanMessage
    


#TBD    ENTER_PROG_MODE_REQ = 0x100
#TBD    REBOOT_REQ_GROUP = 0x101
#TBD    REBOOT_REQ_NODE = 0x102


class HW_TYPE_REQ_GROUP(HapcanMessage):
    # 0xAA 0x103 0x0 MODUL GROUP 0xXX 0xXX 0x00 GROUP 0xXX 0xXX 0xXX 0xXX CHKSUM 0xA5
    FRAME_TYPE = 0x1030

    def __init__(self, senderNode, senderGroup, reqGroup, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.senderNode = senderNode
        self.senderGroup = senderGroup
        self.reqGroup = reqGroup

    @classmethod
    def from_bytes(cls, data: bytearray):
        msg = cls(senderNode=data[3], senderGroup=data[4], reqGroup=data[8])
        return msg

    def to_bytes(self):
        data = bytearray([self.senderNode, self.senderGroup, 0xFF, 0xFF, 0x00, self.reqGroup, 0xFF, 0xFF, 0xFF, 0xFF])
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data
    
    def isFor(self, device):
        return (self.reqGroup == device.groupId) or (self.reqGroup == 0)
    

class HW_TYPE_REQ_GROUP_RESP(HapcanMessage):
    # 0xAA 0x103 0x1 MODULE GROUP HARD1 HARD2 HVER 0xFF ID0 ID1 ID2 ID3 CHKSUM 0xA5
    FRAME_TYPE = 0x1031

    def __init__(self, senderNode, senderGroup, hard, hVer, serialNumber, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.senderNode = senderNode
        self.senderGroup = senderGroup
        self.hard = hard
        self.hVer = hVer
        self.serialNumber = serialNumber

    @classmethod
    def from_bytes(cls, data: bytearray):
        sn = data[9]<<24 | data[10]<<16 | data[11]<<8 | data[12]
        msg = cls(senderNode=data[3], senderGroup=data[4], hard=data[5]<<8 | data[6], hVer=data[7], serialNumber=sn)
        return msg

    def to_bytes(self):
        sn = [(self.serialNumber>>24)&0xFF, (self.serialNumber>>16)&0xFF, (self.serialNumber>>8)&0xFF, self.serialNumber&0xFF]
        data = bytearray([self.senderNode, self.senderGroup, self.hard>>8 & 0xFF, self.hard & 0xFF, self.hVer, 0xFF, *sn])
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data


class HW_TYPE_REQ_NODE(HapcanMessage):
    # 0xAA 0x104 0x0 MODUL GROUP 0xXX 0xXX MODULE GROUP 0xXX 0xXX 0xXX 0xXX CHKSUM 0xA5
    FRAME_TYPE = 0x1040

    def __init__(self, senderNode, senderGroup, reqNode, reqGroup, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.senderNode = senderNode
        self.senderGroup = senderGroup
        self.reqNode = reqNode
        self.reqGroup = reqGroup

    @classmethod
    def from_bytes(cls, data: bytearray):
        msg = cls(senderNode=data[3], senderGroup=data[4], reqNode=data[7], reqGroup=data[8])
        return msg
    
    def to_bytes(self):
        data = bytearray([self.senderNode, self.senderGroup, 0xFF, 0xFF, self.reqNode, self.reqGroup, 0xFF, 0xFF, 0xFF, 0xFF])
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data
    
    def isFor(self, device):
        return (self.reqGroup == device.groupId) and (self.reqNode == device.nodeId)


class HW_TYPE_REQ_NODE_RESP(HapcanMessage):
    # 0xAA 0x104 0x1 MODULE GROUP HARD1 HARD2 HVER 0xFF ID0 ID1 ID2 ID3 CHKSUM 0xA5
    FRAME_TYPE = 0x1041

    def __init__(self, senderNode, senderGroup, hard, hVer, serialNumber, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.senderNode = senderNode
        self.senderGroup = senderGroup
        self.hard = hard
        self.hVer = hVer
        self.serialNumber = serialNumber

    @classmethod
    def from_bytes(cls, data: bytearray):
        sn = data[9]<<24 | data[10]<<16 | data[11]<<8 | data[12]
        msg = cls(senderNode=data[3], senderGroup=data[4], hard=data[5]<<8 | data[6], hVer=data[7], serialNumber=sn)
        return msg
    
    def to_bytes(self):
        sn = [(self.serialNumber>>24)&0xFF, (self.serialNumber>>16)&0xFF, (self.serialNumber>>8)&0xFF, self.serialNumber&0xFF]
        data = bytearray([self.senderNode, self.senderGroup, self.hard>>8 & 0xFF, self.hard & 0xFF, self.hVer, 0xFF, *sn])
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data
    
    def isFor(self, device):
        return (self.senderGroup == device.groupId) and (self.senderNode == device.nodeId)
    

class FW_TYPE_REQ_GROUP(HapcanMessage):
    # 0xAA 0x105 0x0 MODUL GROUP 0xXX 0xXX 0x00 GROUP 0xXX 0xXX 0xXX 0xXX CHKSUM 0xA5
    FRAME_TYPE = 0x1050

    def __init__(self, senderNode, senderGroup, reqGroup, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.senderNode = senderNode
        self.senderGroup = senderGroup
        self.reqGroup = reqGroup

    @classmethod
    def from_bytes(cls, data: bytearray):
        msg = cls(senderNode=data[3], senderGroup=data[4], reqGroup=data[8])
        return msg
    
    def to_bytes(self):
        data = bytearray([self.senderNode, self.senderGroup, 0xFF, 0xFF, 0x00, self.reqGroup, 0xFF, 0xFF, 0xFF, 0xFF])
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data
    
    def isFor(self, device):
        return (self.reqGroup == device.groupId) or (self.reqGroup == 0)


class FW_TYPE_REQ_GROUP_RESP(HapcanMessage):
    # 0xAA 0x105 0x1 MODULE GROUP HARD1 HARD2 HVER ATYPE AVERS FVERS BVER1 BREV2 CHKSUM 0xA5
    FRAME_TYPE = 0x1051

    def __init__(self, senderNode, senderGroup, hard, hVer, aType, aVers, fVers, bootVer, bootRev, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.senderNode = senderNode
        self.senderGroup = senderGroup
        self.hard = hard
        self.hVer = hVer
        self.aType = aType
        self.aVers = aVers
        self.fVers = fVers
        self.bootVer = bootVer
        self.bootRev = bootRev

    @classmethod
    def from_bytes(cls, data: bytearray):
        msg = cls(senderNode=data[3], senderGroup=data[4], hard=data[5]<<8 | data[6], hVer=data[7], aType=data[8], aVers=data[9], fVers=data[10], bootVer=data[11], bootRev=data[12])
        return msg

    def to_bytes(self):
        hard = [self.hard>>8 & 0xFF, self.hard & 0xFF]
        data = bytearray([self.senderNode, self.senderGroup, *hard, self.hVer, self.aType, self.aVers, self.fVers, self.bootVer, self.bootRev])
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data


class FW_TYPE_REQ_NODE(HapcanMessage):
    #0xAA 0x106 0x0 MODULE GROUP 0xXX 0xXX MODULE GROUP 0xXX 0xXX 0xXX 0xXX CHKSUM 0xA5
    FRAME_TYPE = 0x1060

    def __init__(self, senderNode, senderGroup, reqNode, reqGroup, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.senderNode = senderNode
        self.senderGroup = senderGroup
        self.reqNode = reqNode
        self.reqGroup = reqGroup

    @classmethod
    def from_bytes(cls, data: bytearray):
        msg = cls(senderNode=data[3], senderGroup=data[4], reqNode=data[7], reqGroup=data[8])
        return msg

    def to_bytes(self):
        data = bytearray([self.senderNode, self.senderGroup, 0xFF, 0xFF, self.reqNode, self.reqGroup, 0xFF, 0xFF, 0xFF, 0xFF])
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data
    
    def isFor(self, device):
        return (self.reqGroup == device.groupId) and (self.reqNode == device.nodeId)
    

class FW_TYPE_REQ_NODE_RESP(HapcanMessage):
    #0xAA 0x106 0x1 MODULE GROUP HARD1 HARD2 HVER ATYPE AVERS FVERS BVER1 BREV2 CHKSUM 0xA5
    FRAME_TYPE = 0x1061

    def __init__(self, senderNode, senderGroup, hard, hVer, aType, aVers, fVers, bootVer, bootRev, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.senderNode = senderNode
        self.senderGroup = senderGroup
        self.hard = hard
        self.hVer = hVer
        self.aType = aType
        self.aVers = aVers
        self.fVers = fVers
        self.bootVer = bootVer
        self.bootRev = bootRev

    @classmethod
    def from_bytes(cls, data: bytearray):
        msg = cls(senderNode=data[3], senderGroup=data[4], hard=data[5]<<8 | data[6],
                  hVer=data[7], aType=data[8], aVers=data[9], fVers=data[10], bootVer=data[11], bootRev=data[12])
        return msg
    
    def to_bytes(self):
        hard = [self.hard>>8 & 0xFF, self.hard & 0xFF]
        data = bytearray([self.senderNode, self.senderGroup, *hard, self.hVer, self.aType, self.aVers, self.fVers, self.bootVer, self.bootRev])
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data
    

#TBD    INCORRECT_FIRMWARE = 0x1F1
    

class SET_DEFAULT_NODE_AND_GROUP_REQ(HapcanMessage):
    # 0xAA 0x107 0x0 MODUL GROUP 0xXX 0xXX MODULE GROUP 0xXX 0xXX 0xXX 0xXX CHKSUM 0xA5
    FRAME_TYPE = 0x1070

    def __init__(self, senderNode, senderGroup, reqNode, reqGroup, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.senderNode = senderNode
        self.senderGroup = senderGroup
        self.reqNode = reqNode
        self.reqGroup = reqGroup

    @classmethod
    def from_bytes(cls, data: bytearray):
        msg = cls(senderNode=data[3], senderGroup=data[4], reqNode=data[7], reqGroup=data[8])
        return msg
    
    def to_bytes(self):
        data = bytearray([self.senderNode, self.senderGroup, 0xFF, 0xFF, self.reqNode, self.reqGroup, 0xFF, 0xFF, 0xFF, 0xFF])
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data
    
    def isFor(self, device):
        return (self.reqGroup == device.groupId) and (self.reqNode == device.nodeId)
    

class SET_DEFAULT_NODE_AND_GROUP_REQ_RESP(HapcanMessage):
    # 0xAA 0x107 0x1 ID2 ID3 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF CHKSUM 0xA5
    FRAME_TYPE = 0x1071

    def __init__(self, newNodeId, newGroupId, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.newNodeId = newNodeId
        self.newGroupId = newGroupId

    @classmethod
    def from_bytes(cls, data: bytearray):
        msg = cls(newNodeId=data[3], newGroupId=data[4])
        return msg
    
    def to_bytes(self):
        data = bytearray([self.newNodeId, self.newGroupId]) + bytearray(b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF')
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data


########## Messages that can be handled by the functional firmware when bootloader is in normal mode ##########
#TBD    STATUS_REQ_GROUP = 0x108
#TBD    STATUS_REQ_NODE = 0x109
#TBD    CONTROL_MESSAGE = 0x10A
########## Messages that can be handled by the functional firmware when bootloader is in normal mode ##########


class SUPPLY_VOLT_REQ_GROUP(HapcanMessage):
    # 0xAA 0x10B 0x0 MODUL GROUP 0xXX 0xXX 0x00 GROUP 0xXX 0xXX 0xXX 0xXX CHKSUM 0xA5
    FRAME_TYPE = 0x10B0

    def __init__(self, senderNode, senderGroup, reqGroup, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.senderNode = senderNode
        self.senderGroup = senderGroup
        self.reqGroup = reqGroup

    @classmethod
    def from_bytes(cls, data: bytearray):
        msg = cls(senderNode=data[3], senderGroup=data[4], reqGroup=data[8])
        return msg
    
    def to_bytes(self):
        data = bytearray([self.senderNode, self.senderGroup, 0xFF, 0xFF, 0x00, self.reqGroup, 0xFF, 0xFF, 0xFF, 0xFF])
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data
    
    def isFor(self, device):
        return (self.reqGroup == device.groupId) or (self.reqGroup == 0)
    

class SUPPLY_VOLT_REQ_GROUP_RESP(HapcanMessage):
    # 0xAA 0x10B 0x1 MODULE GROUP VOLBUS1 VOLBUS2 VOLCPU1 VOLCPU2 0xFF 0xFF 0xFF 0xFF CHKSUM 0xA5
    FRAME_TYPE = 0x10B1

    def __init__(self, senderNode, senderGroup, rawVBus, rawVCpu, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.senderNode = senderNode
        self.senderGroup = senderGroup
        self.rawVBus = rawVBus
        self.rawVCpu = rawVCpu
    
    @classmethod
    def from_bytes(cls, data: bytearray):
        rawVBus = data[5]<<8 | data[6]
        rawVCpu = data[7]<<8 | data[8]
        msg = cls(senderNode=data[3], senderGroup=data[4], rawVBus=rawVBus, rawVCpu=rawVCpu)
        return msg
    
    def to_bytes(self):
        rawVBus = [self.rawVBus>>8 & 0xFF, self.rawVBus & 0xFF]
        rawVCpu = [self.rawVCpu>>8 & 0xFF, self.rawVCpu & 0xFF]
        data = bytearray([self.senderNode, self.senderGroup, *rawVBus, *rawVCpu, 0xFF, 0xFF, 0xFF, 0xFF])
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data


class SUPPLY_VOLT_REQ_NODE(HapcanMessage):
    # 0xAA 0x10C 0x0 MODUL GROUP 0xXX 0xXX MODULE GROUP 0xXX 0xXX 0xXX 0xXX CHKSUM 0xA5
    FRAME_TYPE = 0x10C0

    def __init__(self, senderNode, senderGroup, reqNode, reqGroup, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.senderNode = senderNode
        self.senderGroup = senderGroup
        self.reqNode = reqNode
        self.reqGroup = reqGroup

    @classmethod
    def from_bytes(cls, data: bytearray):
        msg = cls(senderNode=data[3], senderGroup=data[4], reqNode=data[7], reqGroup=data[8])
        return msg
    
    def to_bytes(self):
        data = bytearray([self.senderNode, self.senderGroup, 0xFF, 0xFF, self.reqNode, self.reqGroup, 0xFF, 0xFF, 0xFF, 0xFF])
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data
    
    def isFor(self, device):
        return (self.reqGroup == device.groupId) and (self.reqNode == device.nodeId)
    

class SUPPLY_VOLT_REQ_NODE_RESP(HapcanMessage):
    # 0xAA 0x10C 0x1 MODULE GROUP VOLBUS1 VOLBUS2 VOLCPU1 VOLCPU2 0xFF 0xFF 0xFF 0xFF CHKSUM 0xA5
    FRAME_TYPE = 0x10C1

    def __init__(self, senderNode, senderGroup, rawVBus, rawVCpu, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.senderNode = senderNode
        self.senderGroup = senderGroup
        self.rawVBus = rawVBus
        self.rawVCpu = rawVCpu

    @classmethod
    def from_bytes(cls, data: bytearray):
        rawVBus = data[5]<<8 | data[6]
        rawVCpu = data[7]<<8 | data[8]
        msg = cls(senderNode=data[3], senderGroup=data[4], rawVBus=rawVBus, rawVCpu=rawVCpu)
        return msg
    
    def to_bytes(self):
        rawVBus = [self.rawVBus>>8 & 0xFF, self.rawVBus & 0xFF]
        rawVCpu = [self.rawVCpu>>8 & 0xFF, self.rawVCpu & 0xFF]
        data = bytearray([self.senderNode, self.senderGroup, *rawVBus, *rawVCpu, 0xFF, 0xFF, 0xFF, 0xFF])
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data


class DESC_REQ_GROUP(HapcanMessage):
    # 0xAA 0x10D 0x0 MODUL GROUP 0xXX 0xXX 0x00 GROUP 0xXX 0xXX 0xXX 0xXX CHKSUM 0xA5
    FRAME_TYPE = 0x10D0

    def __init__(self, senderNode, senderGroup, reqGroup, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.senderNode = senderNode
        self.senderGroup = senderGroup
        self.reqGroup = reqGroup

    @classmethod
    def from_bytes(cls, data: bytearray):
        msg = cls(senderNode=data[3], senderGroup=data[4], reqGroup=data[8])
        return msg
    
    def to_bytes(self):
        data = bytearray([self.senderNode, self.senderGroup, 0xFF, 0xFF, 0x00, self.reqGroup, 0xFF, 0xFF, 0xFF, 0xFF])
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data
    
    def isFor(self, device):
        return (self.reqGroup == device.groupId) or (self.reqGroup == 0)


class DESC_REQ_GROUP_RESP(HapcanMessage):
    # 0xAA 0x10D 0x1 MODULE GROUP abc0 abc1 abc2 abc3 abc4 abc5 abc6 abc7 CHKSUM 0xA5
    FRAME_TYPE = 0x10D1

    def __init__(self, senderNode, senderGroup, desc, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(desc) > 8:
            raise ValueError("Description string too long")
        self.senderNode = senderNode
        self.senderGroup = senderGroup
        self.desc = desc

    @classmethod
    def from_bytes(cls, data: bytearray):
        desc = data[5:13].decode('ascii')
        msg = cls(senderNode=data[3], senderGroup=data[4], desc=desc)
        return msg    
        
    def to_bytes(self):
        data = self.desc.encode('ascii')
        data = bytearray([self.senderNode, self.senderGroup]) + bytearray(data + b'\0'*(8-len(data))) # Make data exactly 8 bytes long
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data


class DESC_REQ_NODE(HapcanMessage):
    # 0xAA 0x10E 0x0 MODULE GROUP 0xXX 0xXX MODULE GROUP 0xXX 0xXX 0xXX 0xXX CHKSUM 0xA5
    FRAME_TYPE = 0x10E0

    def __init__(self, senderNode, senderGroup, reqNode, reqGroup, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.senderNode = senderNode
        self.senderGroup = senderGroup
        self.reqNode = reqNode
        self.reqGroup = reqGroup

    @classmethod
    def from_bytes(cls, data: bytearray):
        msg = cls(senderNode=data[3], senderGroup=data[4], reqNode=data[7], reqGroup=data[8])
        return msg
    
    def to_bytes(self):
        data = bytearray([self.senderNode, self.senderGroup, 0xFF, 0xFF, self.reqNode, self.reqGroup, 0xFF, 0xFF, 0xFF, 0xFF])
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data
    
    def isFor(self, device):
        return (self.reqGroup == device.groupId) and (self.reqNode == device.nodeId)
    

class DESC_REQ_NODE_RESP(HapcanMessage):
    # 0xAA 0x10E 0x1 MODULE GROUP abc0 abc1 abc2 abc3 abc4 abc5 abc6 abc7 CHKSUM 0xA5
    FRAME_TYPE = 0x10E1

    def __init__(self, senderNode, senderGroup, desc, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(desc) > 8:
            raise ValueError("Description string too long")
        self.senderNode = senderNode
        self.senderGroup = senderGroup
        self.desc = desc

    @classmethod
    def from_bytes(cls, data: bytearray):
        desc = data[5:13].decode('ascii')
        msg = cls(senderNode=data[3], senderGroup=data[4], desc=desc)
        return msg    
        
    def to_bytes(self):
        data = self.desc.encode('ascii')
        data = bytearray([self.senderNode, self.senderGroup]) + bytearray(data + b'\0'*(8-len(data))) # Make data exactly 8 bytes long
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data


########## Requests for the processors identification numbers written by Microchip
#TBD    DEVID_REQ_GROUP = 0x10F
#TBD    DEVID_REQ_NODE = 0x111


########## Messages that can be handled by the functional firmware when bootloader is in normal mode ##########
#TBD    UPTIME_REQ_GROUP = 0x112
#TBD    UPTIME_REQ_NODE = 0x113
#TBD    HEALTH_REQ_GROUP = 0x114
#TBD    HEALTH_REQ_NODE = 0x115
########## Messages that can be handled by the functional firmware when bootloader is in normal mode ##########