from modules.interpreter.structures import *


class AstBuilder:
    Ast:list[Token|Loop|Condition] = None

    def __init__(self, code: list[Token]):
        self.Ast = code

    def __json__(self):
        return [t.__dict__() for t in self.Ast]

    def ExtractLoops(self):
        i = 0
        Ast = []
        while i < len(self.Ast):
            loop = self.Ast[i]
            if tk_utils.ValidLoop(loop.subtokens[0]):
                loop = Loop(self.Ast[i : ], Token("end")) 
                e=loop.Exctract()
                i += e
            i += 1
            Ast.append(loop)
        self.Ast = Ast

    def ExtractConditions(self):
        i = 0
        Ast = []
        while i < len(self.Ast):
            cond = self.Ast[i]
            if tk_utils.ValidCondition(cond.subtokens[0]):
                print("here")
                cond = Condition(self.Ast[i : ], Token("end")) 
                e=cond.Exctract()
                i += e
            i += 1
            Ast.append(cond)
        self.Ast = Ast
