from modules.interpreter.statics import *
from modules.interpreter.structures.structure import *

class Goto(Structure):
    def __init__(self, label, condition=None):
        super().__init__([])
        self.type = GOTO
        self.name = "__GOTO__"
        self.label = label.name
        self.condition = condition or []
        self.target = None

    def __dict__(self):
        di = super().__dict__()
        di["label"] = self.label
        di["target"] = self.target
        return di