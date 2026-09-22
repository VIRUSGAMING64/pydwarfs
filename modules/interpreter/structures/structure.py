
from modules.interpreter.tokens.token import *

class Structure(Token):
    expr:list[Token] =  None

    def __init__(self, lines:list[Token]):

        self.subtokens = lines
        
    def __dict__(self):
        sup = super().__dict__()
        sup["Expr"] = [ex.__dict__() for ex in self.expr]
        return sup