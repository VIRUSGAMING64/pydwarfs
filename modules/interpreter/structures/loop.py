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

    def Execute():
        pass

    def EvalCond():
        pass