from modules.interpreter.statics import *
from modules.interpreter.structures.structure import *

class Label(Structure):
    def __init__(self, label):
        super().__init__([])
        self.value = ""
        self.data = {}
        self.type = LABEL
        self.line = label.line
        self.name = label.name.removesuffix(":")

    def __dict__(self):
        di = super().__dict__()
        del di["value"]
        del di["data"]
        return di
    
    def Execute(self, parser):
        return NORMAL, None