
from modules.interpreter.tokens.token import *



#* Exit codes from intructions
NORMAL = 0
FINDING = 2
RETURING = 4




class Structure(Token):
    expr:list[Token] =  None

    def __init__(self, lines:list[Token] , parent = None):
        self.parent = parent
        self.subtokens = lines
        
    def __dict__(self):
        sup = super().__dict__()
        if self.expr == None:
            self.expr = []
        sup["Expr"] = [ex.__dict__() for ex in self.expr]
        return sup