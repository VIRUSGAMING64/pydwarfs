
from modules.interpreter.tokens.token import *

def ToksCompression(tokens: list[Token]):
    s = ""
    for i in tokens:
        s += i.name + " "
    s=s.removesuffix(" ")
    tok = Token(s)
    tok.line = LINE
    tok.subtokens = [tk.copy() for tk in tokens]
    return tok


class Structure(Token):
    expr:list[Token] =  None

    def __init__(self, lines , parent = None):
        super().__init__(ToksCompression(lines).value)
        self.GetType(operations, keywords)
        self.parent = parent
        self.subtokens = lines
        
    def __dict__(self):
        sup = super().__dict__()
        if self.expr == None:
            self.expr = []
        sup["expr"] = [ex.__dict__() for ex in self.expr]
        return sup