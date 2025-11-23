from enum import IntEnum



class Memory:
    class OPERATION(IntEnum):
        READ = 1
        WRITE = 2

    def __init__(self, size, base_address=0x00):
        self.data = bytearray([0xFF]*size)
        self.base_address = base_address

    def read(self, address, length):
        # Adjust address relative to base_address
        idx = address - self.base_address
        return self.data[idx:idx+length]

    def write(self, address, values):
        idx = address - self.base_address
        self.data[idx:idx+len(values)] = values



class FlashMemory(Memory):
    class OPERATION(IntEnum):
        READ = 1
        WRITE = 2
        ERASE = 3

    def __init__(self, size, base_address=0x00, page_size=64):
        super().__init__(size, base_address)
        self.page_size = page_size

    def write(self, address, values):
        idx = address - self.base_address
        for i, byte in enumerate(values):
            old = self.data[idx+i]
            new = byte
            if (old | new) != old:
                raise Exception(f"Flash write requires erase at {address+i}")
            self.data[idx+i] = new

    def erase_page(self, address):
        # Check if address is aligned to page size
        if (address - self.base_address) % self.page_size != 0:
            raise ValueError(f"Address {hex(address)} is not aligned to page size {self.page_size}")

        start = address - self.base_address
        end = start + self.page_size
        for i in range(start, end):
            self.data[i] = 0xFF



class MemoryField:

    def __init__(self, address, size, dtype=int):
        self.address = address
        self.size = size
        self.dtype = dtype # int, str, bytes
        self.name = None # Set by __set_name__

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        mem = instance._get_memory_by_address(self.address)
        raw = mem.read(self.address, self.size)
        if self.dtype == int:
            return int.from_bytes(raw, 'big')
        elif self.dtype == str:
            return raw.decode('ascii', errors='ignore').rstrip('\x00')
        else:
            return raw

    def __set__(self, instance, value):
        mem = instance._get_memory_by_address(self.address)
        if self.dtype == int:
            raw = int(value).to_bytes(self.size, 'big')
        elif self.dtype == str:
            raw = value.encode('ascii', errors='ignore')[:self.size]
            raw = raw.ljust(self.size, b'\x00')
        else:
            raw = value
        mem.write(self.address, raw)