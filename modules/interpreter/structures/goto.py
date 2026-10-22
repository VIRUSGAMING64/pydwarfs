from modules.interpreter.statics import *
from modules.interpreter.structures.structure import *

class Goto(Structure):
    def __init__(self, label):
        super().__init__([])
        self.type = GOTO
        self.line = label.line
        self.name = "__GOTO__"
        self.label = label.name

    def copy(self):
        got = Goto.__new__(Goto)
        got.subtokens = []
        got.type = self.type
        got.name = self.name
        got.label = self.label
        got.line = self.line
        return got

    def __dict__(self):
        di = super().__dict__()
        di["label"] = self.label
        del di["value"]
        del di["data"]
        del di["expr"]
        return di

    def Execute(self, parser):
        return FINDING, self.label