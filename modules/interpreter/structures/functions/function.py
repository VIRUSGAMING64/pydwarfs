
from modules.interpreter.tokens.token import Token, Parser
from modules.interpreter.statics import *
import modules.interpreter.tokens.tokens_utils as tk_utils
from modules.interpreter.exceptions import *
from modules.interpreter.structures.structure import *

class Function(Structure):
    def __init__(self, lines, parent=None):
            self.type = FUNCTION
            base = lines[0]
            self.data = {}
            self.value = ""
            self.name = base.subtokens[1].name 
            self.subtokens = lines[1:]
            self.args = []
            self.line = base.line
            next = True
            for token in base.subtokens[3:-1]:
                if next:
                    if token.type != VARIABLE:
                        raise SintaxisException(
                            f"Invalid function argument [{token.value}]"
                        )
                    self.args.append(token)
                elif token.name != ",":
                    raise SintaxisException(
                        f"Expected comma in function declaration at [{token.value}]"
                    )
                next = not next
                
            if base.subtokens[3:-1] and next:
                raise SintaxisException("Expected function argument after comma")

    def copy(self):
        new = Function.__new__(Function)
        new.value = self.value
        new.data = self.data.copy()
        new.subtokens = [x.copy() for x in self.subtokens]
        new.args = [arg.copy() for arg in self.args]
        new.name = self.name
        new.line = self.line
        new.type = self.type
        return new

    def __dict__(self):
        di = super().__dict__()
        del di["data"]
        del di["value"]
        del di["expr"]
        di["args"] = [arg.__dict__() for arg in self.args]
        return di

    def Execute(self, parser):
        return NORMAL, None