
from modules.interpreter.tokens.token import *

class Structure(Token):
    ender:Token = None
    lines:list[Token] = None
    expr:list[Token] =  None

    def __init__(self, lines:Token, ender : Token):
        self.ender = ender
        self.lines = lines

    def __dict__(self):
        sup = super().__dict__()
        sup["Expr"] = [ex.__dict__() for ex in self.expr]
        return sup