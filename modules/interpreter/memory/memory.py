
import uuid
from modules.interpreter.exceptions import MemoryException

class Memory:
    addrs = {}
    def __init__(self, data = {}):
        self.addrs = data

    def malloc(self, size):
        addr = uuid.uuid4().hex
        self.addrs[addr] = [None] * size
        return addr

    def alloc(self, key, value):
        self.addrs[key] = value

    def query(self, key):
        return self.addrs.get(key, None)

    def realloc(self, addr, size):
        if self.addrs.get(addr) == None:
            #* No existe este addr
            raise MemoryException()

        value = list(self.addrs[addr])
        
        if size < len(self.addrs[addr]):
            value = value[:size]
        while len(value) < size:
            value.append(None)
        self.addrs[addr] = None
        newaddr = uuid.uuid4().hex
        self.addrs[newaddr] = value

