from modules.interpreter.tokens.token import Token
from modules.interpreter.statics import *
import modules.interpreter.tokens.tokens_utils as tk_utils
from modules.interpreter.exceptions import *
from modules.interpreter.structures.structure import *

class Loop(Structure):
    def __init__(self, lines, ender:Token):
        super().__init__(lines, ender)

    def Exctract(self, start = 1) :
        base = self.lines[0]
        if not tk_utils.ValidLoop(base.subtokens[0]):
            raise Exception("Invalid loop extraction")

        self.base_token = base
        self.line = base.line
        self.expr = base.subtokens[1 : ]
        self.type = LOOP
        self.name = "__LOOP__"
        
        i = start

        while i < len(self.lines):
            tok = self.lines[i]

            if self.lines[i].value == self.ender.value:
                loop_code = self.lines[start : i]
                self.subtokens = loop_code
                return i
            
            if tk_utils.ValidLoop(tok):
                loop = Loop(self.lines[i : ], self.ender)
                end = loop.Exctract()
                i += end            

            i+=1

        raise StructureException("Not closed structure")

    def Execute():
        pass

    def EvalCond():
        pass