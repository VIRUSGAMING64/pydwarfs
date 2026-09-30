from modules.interpreter.parser.parserutils import process_op
from modules.interpreter.statics import *
from modules.interpreter.memory import *
from modules.interpreter.exceptions import *
from modules.interpreter.parser.parserutils import *

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

    def copy(self):
        new = Token(
            self.name
        )
        new.subtokens = [sub.copy() for sub in self.subtokens]
        new.value = self.value
        new.line = self.line
        new.type = self.type
        new.data = self.data.copy()
        return new

    def __dict__(self):
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

    def isLabel(self):
        if self.type != NIL:
            return NIL
        self.type = LABEL if self.value.endswith(":") else NIL
        return self.type
    
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
        return NIL | self.IsNum()| self.isLabel() |self.IsOperator(ops) | self.IsKeyword(kwds) | self.VarName() | self.IsString()




class Parser:
    memory: Memory = None
    def __init__(self,mem: Memory):
        self.memory = mem

    def EvalExpr(self, toks:list[Token]):

        #! debug
        print("__________DEBUG__________")
        for i in toks:
            print(i.name,end = " ")
        print("\n__________DEBUG__________")
        #!
        operations = []
        values = []
        unary = True
        for lineidx, elem in enumerate(toks):
            if elem.type & COMMENT:
                continue

            if elem.type & VARIABLE:
                value = self.memory.query(elem.name)
                if value == None and (lineidx != 0 or toks[lineidx + 1].value != "="):
                    raise Exception("Variable not declared")
                elem.value = value
                
            if elem.name == "(":
                operations.append(elem)
                unary = True
        
            elif elem.name == ")":  
                if len(operations) == 0:
                    raise ExpresionException(toks)
                while operations[-1].name != "(":
                    self.process(values, operations, None)

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
            self.process(values,operations, -1)

        if len(values) > 1 or len(operations)!=0:
            raise ExpresionException("Invalid expression")
        
        if len(values) == 0:
            val = Token(0)
            val.GetType(operators, keywords)
            return val
        
        return values[0]

    def process(self, nums, oper , li = None):
        try:
            
            for i in nums:
                print("num: ",i.__dict__())
                
            for i in oper:
                print("oper: ",i.__dict__())

            a = nums.pop()
            opp = oper.pop()
            if opp.data.get("neg", False):
                res = UnaryOP(a,  opp)
                res = Token( res)
                res.GetType(operators,keywords)
                nums.append(res)
                return
    
            b = nums.pop()        
            n = process_op(a, b, opp, self.memory)
            if n == None:
                #* se esta haciendo una asignacion de valor 
                nums.append(b)
                print(b.__dict__())
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
        
