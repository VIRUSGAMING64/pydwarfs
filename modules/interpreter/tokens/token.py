from modules.interpreter.statics import *

class Token:
    subtokens: list[Token] = None
    value:str = None
    type = 0
    name = None
    line = -1
    data = None
    
    def __init__(self,expr):
        self.data = {}
        self.value = expr
        self.name = expr
        self.subtokens = []

    def __dict__(self):
        return {
            "name": self.name,
            "type": self.type,
            "line": self.line,
            "value": self.value,
            "data": self.data,
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
        if isinstance(self.value, int):
            self.type = NUMBER
            self.value = int(self.value)
            return self.value
        if not isinstance(self.value, str):
            return NIL
        if self.value.isnumeric():
            self.type = NUMBER
            self.value = int(self.value)
            return self.value
        return NIL
    
    def GetType(self, ops, kwds):
        return NIL | self.IsNum()|self.IsOperator(ops) | self.IsKeyword(kwds) | self.VarName() | self.IsString()

    