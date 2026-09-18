from modules.interpreter.statics import *

class Token:
    subtokens: list[Token] = []
    value:str = None
    type = 0
    name = None
    line = -1
    def __init__(self,expr):
        self.value = expr
        self.name = expr

    def __dict__(self):
        return {
            "name": self.name,
            "type": self.type,
            "line": self.line,
            "value": self.value,
            "subtokens": [token.__dict__() for token in self.subtokens]
        }


    def VarName(self):
        if self.type != NIL:
            return NIL
        alphas = ""
        for i in self.value:
            if i.isalnum():
                alphas+=i
            elif i != "_":
                return NIL
        
        if(alphas[0].isnumeric()):
            return NIL

        if len(alphas) >= 1:
            self.type = VARIABLE
            return VARIABLE
        
        print(alphas)
        return NIL

    def IsKeyword(self, kwds):
        if self.type != NIL:
            return NIL
        if self.value in kwds:
            self.type=KEYWORD
        return self.type    

    def IsOperator(self,ops):
        if self.type != NIL:
            return NIL
        if self.value in ops:
            self.type = OPERATOR
            return self.type
        return NIL

    def IsAlnum(self):
        if self.type != NIL:
            return NIL
        if not isinstance(self.value,str):
            return NIL
        if self.value.isalnum():
            self.type = VARIABLE
            return VARIABLE
        return NIL
    
    def IsString(self):
        if self.type != NIL:
            return NIL
        if not isinstance(self.value, str):
            return NIL
        return STRING

    def IsNum(self):
        if self.type != NIL:
            return NIL
        if not isinstance(self.value, str):
            return NIL
        if self.value.isnumeric():
            self.type = NUMBER
            self.type = int(self.type)
            return self.type
        return NIL
    
    def GetType(self, ops, kwds):
        return self.IsOperator(ops) | self.IsAlnum() | self.IsString() | self.IsNum() | self.IsKeyword(kwds) | self.VarName()

    