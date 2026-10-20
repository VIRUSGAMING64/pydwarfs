from modules.interpreter.tokens.token import Token, Parser
from modules.interpreter.statics import *
import modules.interpreter.tokens.tokens_utils as tk_utils
from modules.interpreter.exceptions import *
from modules.interpreter.structures.structure import *

class Condition(Structure):
    def __init__(self, lines):
        super().__init__(lines[1:])
        base = lines[0]
        self.base_token = base
        self.line = base.line
        self.type = CONDITION
        self.name = "__CONDITION__"
        self.expr = base.subtokens[1 : ]
        self.value = ""
        self.data ={}
        self.ip = 0

    def __dict__(self):
        di = super().__dict__()
        del di["value"]
        del di["data"]
        return di

    def copy(self):
        cond = Condition.__new__(Condition)
        cond.base_token = self.base_token
        cond.data = self.data
        cond.ip = 0
        cond.value = ""
        cond.line = self.line
        cond.expr = self.expr
        cond.name = self.name
        cond.type = self.type
        cond.subtokens = [x.copy() for x in self.subtokens]
        return cond

    def IsGoto(self):
        for i,elem in enumerate(self.base_token.subtokens):
            if elem.name == "goto":
                self.subtokens = self.base_token.subtokens[i : ]
                self.expr = self.base_token.subtokens[1:i]
                return True
        return False

    def Execute(self, parser: Parser):  
        if self.ip == 0:
            if not self.EvalCond(parser):
                return NORMAL,None
        if len(self.subtokens) == self.ip:
            input()
            
        expr = self.subtokens[self.ip]
        re = expr.Execute(parser)
        code, val = re[0], re[1]
        if code != NORMAL:
            self.ip=0
            return code,val
        
        self.ip += 1
        self.ip %= len(self.subtokens)
        if self.ip == 0:    
            return NORMAL, None
                
        return CONTINUE, None

    def EvalCond(self,parser: Parser):
        opcode, tok = parser.EvalExpr(self.expr)
        return tok.value