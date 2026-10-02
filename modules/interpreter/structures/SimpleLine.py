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

    def IsGoto(self):
        for i,elem in enumerate(self.base_token.subtokens):
            if elem.name == "goto":
                self.subtokens = self.base_token.subtokens[i : ]
                self.expr = self.base_token.subtokens[1:i]
                return True
        return False

    def Execute(self, parser: Parser):
        val = parser.EvalExpr(self.subtokens)
        return NORMAL, None
    
    def __dict__(self):
        di = super().__dict__()
        del di["value"]
        del di["data"]
        return di