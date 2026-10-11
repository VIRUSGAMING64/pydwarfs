from modules.interpreter.parser.parserutils import process_op
from modules.interpreter.statics import *
from modules.interpreter.memory import *
from modules.interpreter.exceptions import *
from modules.interpreter.parser.parserutils import *


class Token:
    subtokens: list[Token]
    value:str
    type = 0
    name:str
    line :int = -1
    data:dict 

    def Execute(self,parser):
        print(self.__dict__())
        raise Exception("Token not executable")
        return NORMAL, None
    
    def __init__(self,expr, type=None):
        self.data = {}
        self.value = expr
        self.name = expr
        self.subtokens = []
        if type != None:
            self.type = type

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
        flag = False
        for c in ["'", '"']:
            if self.value.startswith(c):
                flag = True

        if flag:
            self.type = STRING

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


class Parser:
    memory: Memory
    def __init__(self,mem: Memory):
        self.memory = mem

    def EvalExpr(self, toks:list[Token]):
        operations = []
        values = []
        unary = True

        for lineidx, elem in enumerate(toks):
            assert elem is not None
            if elem.type & FUNCCALL:
                elem = elem.Execute(self,self.memory)
                assert elem is not None
                toks[lineidx] = elem

        for lineidx, elem in enumerate(toks):
            print(elem.name,end = " ")
            if elem != None and (elem.type & VARIABLE):
                value = self.memory.query(elem.name)
                is_assignment = (
                    lineidx + 1 < len(toks) and toks[lineidx + 1].value == "="
                )
                if value == None and not is_assignment:
                    raise MissingVariable(elem.name)
                if value != None:
                    elem.value = value.value
        print("\n")
        for lineidx, elem in enumerate(toks):       
            if elem.name == "(":
                operations.append(elem)
                unary = True
        
            elif elem.name == ")":  
                if len(operations) == 0:
                    raise ExpresionException("Invalid expresion at line")
                while operations[-1].name != "(":
                    self.process(values, operations)

                operations.pop()
                unary = False
                
            elif IsOperator(elem):
                if unary and is_unary(elem):
                    elem.data["neg"] = True
                
                while (len(operations)>0 and (
                        ((getPrio(operations[-1]) >= getPrio(elem)) and (elem.data.get("neg",False) >= 0)) or
                        (elem.data.get("neg",False) < 0 and ((getPrio(operations[-1])) >= getPrio(elem)))
                    )):
                    self.process(values, operations)

                unary = True
                operations.append(elem)
            else:
                unary = False
                values.append(elem)

   
        while len(operations) > 0:
            self.process(values,operations)

        if len(values) > 1 or len(operations)!=0:
            raise ExpresionException("Invalid expression")
        
        if len(values) == 0:
            val = Token(0)
            val.GetType(operators, keywords)
            return NORMAL,val
        
        return NORMAL,values[0]

    def process(self, nums, oper):
        try:
            a = nums.pop()
            opp = oper.pop()
            if opp.data.get("neg", False):
                res =  Token( UnaryOP(a,  opp) )
                res.GetType(operators,keywords)
                nums.append(res)
                return
    
            b = nums.pop()        
            n = process_op(a, b, opp, self.memory)
            if n == None:
                #* se esta haciendo una asignacion de valor 
                nums.append(b)
                return
            
            res = Token(n)
            res.GetType(operators, keywords)
            nums.append(res)
        except Exception as e:
            if isinstance(e, IndexError):
                raise ExpresionException("Invalid expression")
            if isinstance(e , ZeroDivisionError):
                raise ZeroDivisionException('Zero division')
            raise e
        
