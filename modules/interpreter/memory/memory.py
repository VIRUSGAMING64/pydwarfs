
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
        self.addrs[key] = value.copy()

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
        del self.addrs[addr]
        newaddr = uuid.uuid4().hex
        self.addrs[newaddr] = value
        return newaddr

    def __dict__(self):
        di = {}
        for i in self.addrs:
            if not isinstance(self.addrs[i], int|str):
                di[i] = self.addrs[i].copy() #* Aqui hay q ver si es una clase luego
            else:
                di[i] = self.addrs[i]
        return di