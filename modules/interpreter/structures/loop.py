from modules.interpreter.tokens.token import Token
from modules.interpreter.statics import *
import modules.interpreter.tokens.tokens_utils as tk_utils
from modules.interpreter.exceptions import *
from modules.interpreter.structures.structure import *

class Loop(Structure):
    def __init__(self, lines, parent = None):
        super().__init__(lines[1:], parent)
        base = lines[0]
        self.base_token = base
        self.line = base.line
        self.type = LOOP
        self.name = "__LOOP__"
        self.expr = base.subtokens[1 : ]
        self.ip = 0

    def Execute(self, parser: Parser):  
            if self.ip == 0:
                if not self.EvalCond(parser):
                    return NORMAL,None
            l=self.ip
            self.ip = 0
            expr=self.subtokens[l]
            code, val = expr.Execute(parser)        
            if code != NORMAL:
                return code,val
            self.ip = (l + 1) % len(self.subtokens)
            return CONTINUE, None

    def EvalCond(self,parser: Parser):
        tok = parser.EvalExpr(self.expr)
        return tok.value