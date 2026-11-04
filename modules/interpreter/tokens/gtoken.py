from modules.interpreter.parser.parserutils import process_op
from modules.interpreter.statics import *

class Token:
    subtokens: list[Token]
    value:str
    type = 0
    name:str
    line :int = -1
    data:dict 

    def Execute(self,parser):
        raise Exception("Token not executable")
        return NORMAL, None
    
    def __init__(self,expr, tp=None):
        self.data = {}
        self.value = expr
        self.name = expr
        self.subtokens = []
        if tp != None:
            self.type = tp

    def copy(self):
        new = Token(
            self.name
        )
        new.subtokens = [sub.copy() for sub in self.subtokens]
        new.value = self.value
        new.line = self.line
        new.type = self.type
        if self.data == None:
            self.data = {}
        new.data = self.data.copy()
        return new

    def __dict__(self) :
        if self.subtokens == None:
            self.subtokens = []
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
        if alphas == "":
            return NIL
        if(alphas[0].isnumeric()):
            return NIL

        if len(alphas) >= 1:
            self.type = VARIABLE
            return VARIABLE
        
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
        flag = False
        for c in ["'", '"']:
            if self.value.startswith(c):
                flag = True

        if flag:
            self.type = STRING
            self.value = self.value[1:-1]

        return self.type

    def isLabel(self):
        if self.type != NIL:
            return NIL
        self.type = LABEL if self.value.endswith(":") else NIL
        if self.type & LABEL:
            self.name = self.name.removesuffix(":")
           
        return self.type
    
    def IsNum(self):
        if self.type != NIL:
            return NIL
        if isinstance(self.value, int):
            self.type = NUMBER
            self.value = int(self.value) # type: ignore
            return NUMBER
        if not isinstance(self.value, str):
            return NIL
        if self.value.isnumeric():
            self.type = NUMBER
            self.value = int(self.value) # type: ignore
            return NUMBER
        return NIL
    
    def GetType(self, ops, kwds):
        return NIL | self.IsNum()| self.isLabel() |self.IsOperator(ops) | self.IsKeyword(kwds) | self.VarName() | self.IsString()

