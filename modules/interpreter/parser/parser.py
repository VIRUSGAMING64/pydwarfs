from modules.interpreter.parser.parserutils import process_op
from modules.interpreter.statics import *
from modules.interpreter.memory import *
from modules.interpreter.exceptions import *
from modules.interpreter.parser.parserutils import *
from modules.interpreter.tokens.gtoken import *

class Parser:
    memory: Memory
    def __init__(self,mem: Memory):
        self.memory = mem

    def EvalExpr(self, tokens:list[Token]):
        toks = [x.copy() for x in tokens]
        operations = []
        values = []
        unary = True

        for lineidx, elem in enumerate(toks):
            assert elem is not None
            if elem.type & FUNCCALL:
                code, elem = elem.Execute(self,self.memory)
                if not (code & NORMAL):
                    return code, None
                assert elem is not None
                toks[lineidx] = elem

        for lineidx, elem in enumerate(toks):
            if elem != None and (elem.type & VARIABLE):
                value = self.memory.query(elem.name)
                is_assignment = (
                    lineidx + 1 < len(toks) and toks[lineidx + 1].value == "="
                )
                expr = toks[lineidx+2 : ]
                if len(expr) >= 1 and is_assignment:
                    a_value = self.EvalExpr(expr)[1]
                    elem.type |= a_value.type
                    toks = toks[:lineidx+2] + [a_value]
                    break

                if value == None and not is_assignment:
                    raise MissingVariable(elem.name)

                if value != None:
                    elem.value = value.value
                    elem.type |= value.type

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
                if elem.name == "!" and not unary:
                    raise ExpresionException(
                        f"Operator [{elem.value}] must be unary"
                    )
                if unary and is_unary(elem):
                    elem.data["neg"] = True
                
                while (len(operations)>0 and (
                        ((getPrio(operations[-1]) > getPrio(elem)) and (elem.data.get("neg",False) >= 0)) or
                        (elem.data.get("neg",False) < 0 and ((getPrio(operations[-1])) >= getPrio(elem))) or
                        (getPrio(operations[-1]) == getPrio(elem) and elem.value != "**")
                    )):
                    self.process(values, operations)

                unary = True
                operations.append(elem)
            else:
                unary = False
                values.append(elem)
   
        while len(operations) > 0:
            self.process(values,operations)


        if len(values) < 1 or len(values) > 1 or len(operations)!=0:
            raise ExpresionException("Invalid expression")
            
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
            if isinstance(e, KeyError):
                raise ExpresionException(f"Invalid operator [{opp.value}]")
            if isinstance(e, IndexError):
                raise SintaxisException("Invalid expression")
            if isinstance(e , ZeroDivisionError):
                raise ZeroDivisionException('Zero division')
            raise e
        
