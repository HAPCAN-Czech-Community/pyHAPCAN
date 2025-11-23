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


#TBD    ADDRESS_FRAME = 0x030
#TBD    DATA_FRAME = 0x040
