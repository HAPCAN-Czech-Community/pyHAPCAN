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


class EXIT_ONE_BOOTLOADER(HapcanMessage):
    # 0xAA 0x020 0x0 MODULE GROUP 0xXX 0xXX 0xXX 0xXX 0xXX 0xXX 0xXX 0xXX CHKSUM 0xA5
    FRAME_TYPE = 0x0200

    def __init__(self, targetNode, targetGroup, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.targetNode = targetNode
        self.targetGroup = targetGroup

    @classmethod
    def from_bytes(cls, data: bytearray):
        msg = cls()
        return msg
    
    def to_bytes(self):
        data = bytearray([self.targetNode, self.targetGroup]) + bytearray(b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF')
        self._prepend_type(data, self.FRAME_TYPE)
        self._append_checksum(data)
        self._append_header_trailer(data)
        return data
    

#TBD    ADDRESS_FRAME = 0x030
#TBD    DATA_FRAME = 0x040