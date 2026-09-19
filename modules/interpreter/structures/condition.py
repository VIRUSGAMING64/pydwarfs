from modules.interpreter.tokens.token import Token
from modules.interpreter.statics import *
import modules.interpreter.tokens.tokens_utils as tk_utils
from modules.interpreter.exceptions import *
from modules.interpreter.structures.structure import *

class Condition(Structure):
    def __init__(self, lines, ender:Token):
        super().__init__(lines, ender)

    def Exctract(self, start = 1) :
        base = self.lines[0]
        if not tk_utils.ValidCondition(base.subtokens[0]):
            raise Exception("Invalid condition extraction")

        self.base_token = base
        self.line = base.line
        self.type = CONDITION
        self.name = "__CONDITION__"
        self.expr = base.subtokens[1 : ]
                
        for i,elem in enumerate(base.subtokens):
            if elem.name == "goto":
                self.subtokens = base.subtokens[i : ]
                self.expr = base.subtokens[1:i]
                return start
        i = start

        while i < len(self.lines):
            tok = self.lines[i]

            if self.lines[i].value == self.ender.value:
                loop_code = self.lines[start : i]
                self.subtokens = loop_code
                return i
            
            if tk_utils.ValidCondition(tok):
                loop = Condition(self.lines[i : ], self.ender)
                end = loop.Exctract()
                i += end            

            i+=1
        
        raise StructureException("Not closed structure")

    def Execute():
        pass

    def EvalCond():
        pass