from .hapcanMessage import HapcanMessage
from .hapcanMemory import Memory, FlashMemory, MemoryField


class HapcanDevice:
    
    # Prepare memory-mapped fields
    serialNumber   = MemoryField(address=0x000024, size=4)
    hard           = MemoryField(address=0x001010, size=2)
    hVer           = MemoryField(address=0x001012, size=1)
    aType          = MemoryField(address=0x001013, size=1)
    aVers          = MemoryField(address=0x001014, size=1)
    fVers          = MemoryField(address=0x001015, size=1)
    bootVer        = MemoryField(address=0x001016, size=1)
    bootRev        = MemoryField(address=0x001017, size=1)
    nodeId         = MemoryField(address=0xF00026, size=1)
    groupId        = MemoryField(address=0xF00027, size=1)
    description    = MemoryField(address=0xF00030, size=16, dtype=str)
    #rawVBus       # In real devices, these are immediately converted from ADC when requested
    #rawVCpu       # In real devices, these are immediately converted from ADC when requested

    def __init__(self, emulator, nodeId, groupId, serialNumber, aType,
                 hard=0x3000, hVer=0x03, aVers=0x00, fVers=0x00,
                 bootVer=0x00, bootRev=0x00, description="",
                 rawVBus=0x0000, rawVCpu=0x0000):
        
        # List of field names that must fit in 0–255
        byte_fields = [
            "nodeId",
            "groupId",
            "hVer",
            "aType",
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
        
        self._emulator = emulator
        
        # Initialize memories
        self.eeprom = Memory(size=(0xF003FF - 0xF00000 + 1), base_address=0xF00000)  # 0xF00000 - 0xF003FF
        self.flash = FlashMemory(size=(0x00FFFF - 0x000000 + 1), base_address=0x000000, page_size=64)  # 0x000000 - 0x00FFFF

        self._mem_cmd = Memory.OPERATION.READ
        self._mem_addr = 0

        # Set initial values
        self.serialNumber = serialNumber
        self.hard = hard
        self.hVer = hVer
        self.aType = aType
        self.aVers = aVers
        self.fVers = fVers
        self.bootVer = bootVer
        self.bootRev = bootRev
        self.nodeId = nodeId
        self.groupId = groupId
        self.description = description
        self.rawVBus = rawVBus
        self.rawVCpu = rawVCpu


    def _get_memory_by_address(self, addr):
        for mem in [self.eeprom, self.flash]:
            if mem.base_address <= addr < mem.base_address + len(mem.data):
                return mem
        raise ValueError(f"Address {hex(addr)} is outside memory ranges")


    def processCanApplicationMessage(self, m: HapcanMessage):
         # If this is NOT an instance of HapcanDevice itself, complain
        if type(self) is not HapcanDevice:
            raise NotImplementedError(f"{self.__class__.__name__} must implement processCanApplicationMessage()")
        

    def processCanMessage(self, m: HapcanMessage):
        # Process programming messages
        if m.FRAME_TYPE == HapcanMessage.EXIT_ALL_BOOTLOADER.FRAME_TYPE:
            if m.isFor(self):
                return
        
        elif m.FRAME_TYPE == HapcanMessage.EXIT_ONE_BOOTLOADER.FRAME_TYPE:
            if m.isFor(self):
                return
        
        elif m.FRAME_TYPE == HapcanMessage.ADDRESS_FRAME.FRAME_TYPE:
            if m.isFor(self):
                self._mem_addr = m.addr
                self._mem_cmd = m.cmd
                resp = m.makeResponse()
                self.sendCanMessage(resp)
                return

        elif m.FRAME_TYPE == HapcanMessage.DATA_FRAME.FRAME_TYPE:
            if m.isFor(self):
                mem = self._get_memory_by_address(self._mem_addr)

                if self._mem_cmd == mem.OPERATION.READ:
                    dataBytes = mem.read(self._mem_addr, 8)
                    resp = HapcanMessage.DATA_FRAME_RESP(targetNode=self.nodeId, targetGroup=self.groupId, dataBytes=dataBytes)

                elif self._mem_cmd == mem.OPERATION.WRITE:
                    mem.write(self._mem_addr, m.dataBytes)
                    dataBytes = mem.read(self._mem_addr, 8)
                    resp = HapcanMessage.DATA_FRAME_RESP(targetNode=self.nodeId, targetGroup=self.groupId, dataBytes=dataBytes)

                elif self._mem_cmd == mem.OPERATION.ERASE:
                    mem.erase_page(self._mem_addr)
                    dataBytes = mem.read(self._mem_addr, 8)
                    resp = HapcanMessage.DATA_FRAME_RESP(targetNode=self.nodeId, targetGroup=self.groupId, dataBytes=dataBytes)

                self.sendCanMessage(resp)
                return
        

        # Process system messages
        elif m.FRAME_TYPE == HapcanMessage.ENTER_PROG_MODE_REQ.FRAME_TYPE:
            if m.isFor(self):
                resp = HapcanMessage.ENTER_PROG_MODE_REQ_RESP(senderNode=self.nodeId, senderGroup=self.groupId,
                                                              bootVer=self.bootVer, bootRev=self.bootRev)
                self.sendCanMessage(resp)
                return

        elif m.FRAME_TYPE == HapcanMessage.HW_TYPE_REQ_GROUP.FRAME_TYPE:
            if m.isFor(self):
                resp = HapcanMessage.HW_TYPE_REQ_GROUP_RESP(senderNode=self.nodeId, senderGroup=self.groupId,
                                                            hard=self.hard, hVer=self.hVer, serialNumber=self.serialNumber)
                self.sendCanMessage(resp)
                return
        
        elif m.FRAME_TYPE == HapcanMessage.HW_TYPE_REQ_NODE.FRAME_TYPE:
            if m.isFor(self):
                resp = HapcanMessage.HW_TYPE_REQ_NODE_RESP(senderNode=self.nodeId, senderGroup=self.groupId,
                                                           hard=self.hard, hVer=self.hVer, serialNumber=self.serialNumber)
                self.sendCanMessage(resp)
                return
        
        elif m.FRAME_TYPE == HapcanMessage.FW_TYPE_REQ_GROUP.FRAME_TYPE:
            if m.isFor(self):
                resp = HapcanMessage.FW_TYPE_REQ_GROUP_RESP(senderNode=self.nodeId, senderGroup=self.groupId,
                                                           hard=self.hard, hVer=self.hVer, aType=self.aType,
                                                           aVers=self.aVers, fVers=self.fVers,
                                                           bootVer=self.bootVer, bootRev=self.bootRev)
                self.sendCanMessage(resp)
                return
        
        elif m.FRAME_TYPE == HapcanMessage.FW_TYPE_REQ_NODE.FRAME_TYPE:
            if m.isFor(self):
                resp = HapcanMessage.FW_TYPE_REQ_NODE_RESP(senderNode=self.nodeId, senderGroup=self.groupId,
                                                           hard=self.hard, hVer=self.hVer, aType=self.aType,
                                                           aVers=self.aVers, fVers=self.fVers,
                                                           bootVer=self.bootVer, bootRev=self.bootRev)
                self.sendCanMessage(resp)
                return
        
        elif m.FRAME_TYPE == HapcanMessage.SET_DEFAULT_NODE_AND_GROUP_REQ.FRAME_TYPE:
            if m.isFor(self):
                # Set node and group to default values derived from serial number
                self.nodeId = self.serialNumber>>8 & 0xFF
                self.groupId = self.serialNumber & 0xFF
                resp = HapcanMessage.SET_DEFAULT_NODE_AND_GROUP_REQ_RESP(newNodeId=self.nodeId, newGroupId=self.groupId)
                self.sendCanMessage(resp)
                return

        elif m.FRAME_TYPE == HapcanMessage.SUPPLY_VOLT_REQ_GROUP.FRAME_TYPE:
            if m.isFor(self):
                resp = HapcanMessage.SUPPLY_VOLT_REQ_GROUP_RESP(senderNode=self.nodeId, senderGroup=self.groupId,
                                                                rawVBus=self.rawVBus, rawVCpu=self.rawVCpu)
                self.sendCanMessage(resp)
                return

        elif m.FRAME_TYPE == HapcanMessage.SUPPLY_VOLT_REQ_NODE.FRAME_TYPE:
            if m.isFor(self):
                resp = HapcanMessage.SUPPLY_VOLT_REQ_NODE_RESP(senderNode=self.nodeId, senderGroup=self.groupId,
                                                               rawVBus=self.rawVBus, rawVCpu=self.rawVCpu)
                self.sendCanMessage(resp)
                return
        
        elif m.FRAME_TYPE == HapcanMessage.DESC_REQ_GROUP.FRAME_TYPE:
            if m.isFor(self):
                desc0 = self.description[0:8]
                desc1 = self.description[8:16]
                resp0 = HapcanMessage.DESC_REQ_GROUP_RESP(senderNode=self.nodeId, senderGroup=self.groupId, desc=desc0)
                resp1 = HapcanMessage.DESC_REQ_GROUP_RESP(senderNode=self.nodeId, senderGroup=self.groupId, desc=desc1)
                self.sendCanMessage(resp0)
                self.sendCanMessage(resp1)
                return
        
        elif m.FRAME_TYPE == HapcanMessage.DESC_REQ_NODE.FRAME_TYPE:
            if m.isFor(self):
                desc0 = self.description[0:8]
                desc1 = self.description[8:16]
                resp0 = HapcanMessage.DESC_REQ_NODE_RESP(senderNode=self.nodeId, senderGroup=self.groupId, desc=desc0)
                resp1 = HapcanMessage.DESC_REQ_NODE_RESP(senderNode=self.nodeId, senderGroup=self.groupId, desc=desc1)
                self.sendCanMessage(resp0)
                self.sendCanMessage(resp1)
                return
        
        
        # Forward other messages to application message processing
        self.processCanApplicationMessage(m)


    def process(self):
        # May be handled by subclasses which need to process something in a loop
        pass


    def sendCanMessage(self, message:HapcanMessage):
        message._sender = self
        self._emulator.broadcastCanMessage(message)