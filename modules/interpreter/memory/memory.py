from modules.interpreter.exceptions import MemoryException

class Memory:
    addrs : dict
    consts: dict
    def __init__(self, data = None):
        if data == None:
            data = {}
        self.addrs = data
        self.consts = {}

    def copy(self):
        mem = Memory()
        mem.addrs = {}
        
        for key in self.addrs:
            mem.addrs[key] = self.addrs[key].copy()

        for key in self.consts:
            mem.consts[key] = self.consts[key]

        return mem

    def alloc_const(self, key, value):
        self.consts[key] = True
        self.addrs[key] = value.copy()
    
    def alloc(self, key, value):
        if self.addrs.get(key,None) != None:
            
            if self.consts.get(key, False):
                raise MemoryException("Cannot eddit constants")

            self.addrs[key].value = value.value
        else:
            self.addrs[key] = value.copy()

    def query(self, key):
        val = self.addrs.get(key, None)
        if val != None:
            return  val.copy()
        return val
    
    def __dict__(self):
        di = {}
        for i in self.addrs:
            if not isinstance(self.addrs[i], int|str):
                di[i] = self.addrs[i].copy().__dict__() #* Aqui hay q ver si es una clase luego
            else:
                di[i] = self.addrs[i]
        return di