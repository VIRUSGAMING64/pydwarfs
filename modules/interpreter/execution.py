from modules.interpreter.memory import *
from modules.interpreter.tokens import *
from modules.interpreter.exceptions import *

class Parser:
    def EvalExpr(self, toks:list[Token]):
        operations = []
        values = []
        unary = True
        for lineidx, elem in enumerate(toks):
            if elem.type & COMMENT:
                continue

            if elem.type & VARIABLE:
                data = self.memory.query(elem.name)
                
            elif elem.name == "(":
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
        
        while len(operations):
            self.process(values,operations, -1)

        if len(values) > 1 or len(operations)!=0:
            raise ExpresionException("Invalid expression")
        
        if len(values) == 0:
            return Token(0, NUMBER)
        
        return values[0]

    def process(self, nums, oper , li = None):
        try:
            a = nums.pop()
            opp = oper.pop()
            if opp.data.get("neg", False):
                res = UnaryOP(a,  opp)
                res = Token( res)
                res.GetType(operators,keywords)
                nums.append(res)
                return
            b = nums.pop()        
            n = process_op(a, b, opp, None)
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
        