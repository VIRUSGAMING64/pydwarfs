from modules.interpreter.tokens.token import Token, Parser
from modules.interpreter.statics import *
import modules.interpreter.tokens.tokens_utils as tk_utils
from modules.interpreter.exceptions import *
from modules.interpreter.structures.structure import *

class SingleLine(Structure):
    def __init__(self, lines):
        super().__init__(lines[1:])
        base = lines[0]
        self.base_token = base
        self.line = base.line
        self.type = LINE
        self.name = "__LINE__"
        self.value = self.name
        self.data = {}
    
    def __dict__(self):
        di = super().__dict__()
        del di["value"]
        del di["data"]
        del di["expr"]
        return di