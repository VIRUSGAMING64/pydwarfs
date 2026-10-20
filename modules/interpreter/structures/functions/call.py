
from modules.interpreter.tokens.token import Token, Parser
from modules.interpreter.statics import *
import modules.interpreter.tokens.tokens_utils as tk_utils
from modules.interpreter.exceptions import *
from modules.interpreter.structures.structure import *
from modules.interpreter.statics import *
from modules.interpreter.structures.functions.builtin import *
class FuncCall(Structure):
    args: list[Token]
    def __init__(self, name, args, line):
        if not isinstance(args, list):
            raise Exception("args not is a list")
        self.type = FUNCCALL
        self.args = args
        self.name = name
        self.line = line
        self.subtokens = []
        self.value = ""
        self.isbuiltin = 0
        self.data = {}

    def copy(self):
        f = FuncCall(self.name, self.args, self.line)
        f.isbuiltin = self.isbuiltin
        return f
        
    def __dict__(self):
        di = super().__dict__()
        del di["data"]
        del di["value"]
        del di["expr"]
        del di["subtokens"]
        di["isbuiltin"] = self.isbuiltin
        di["args"] = []
        for a in self.args:
            t = []
            for i in a:
                t.append(i.__dict__()) 
            di["args"].append(t)  
        return di

    def Execute(self,parser, mem:Memory):
    
        if len(self.args) > 0:   
            args = [parser.EvalExpr(argument)[1] for argument in self.args]

        if self.isbuiltin:

            if len(args) != argslens[self.name]:
                raise CallFuncException(
                    f"Invalid number of arguments for [{self.name}]"
                )
            #! Para debug

            res = builtinfuncs[self.name](mem, args)

            
            if res == None:
                res = 0

            return Token(res, NUMBER)
        
        
        func = mem.query(self.name)
        
        if func is None:
            raise MissingVariable(self.name)
        
        if not (func.type & FUNCTION):
            raise MissingVariable(self.name)
        args = []
        
        if len(args) != len(func.args):
            raise CallFuncException(
                f"Invalid number of arguments for [{self.name}]"
            )


        local_memory = Memory()
        for i,value in enumerate(args):
            local_memory.alloc(func.args[i].name, value)

        # Function definitions remain visible so recursive calls can resolve.
        for name, value in parser.memory.addrs.items():
            if value.type & FUNCTION:
                local_memory.addrs[name] = value
            if local_memory.query(name) == None:
                local_memory.addrs[name] = mem.addrs[name]
        
        local_parser = Parser(local_memory)
        idx = 0 
        while idx < len(func.subtokens):
            statement = func.subtokens[idx]
            if statement.subtokens[0].value == "ret":
                cl =  local_parser.EvalExpr(statement.subtokens[1:])[1].copy()
                R = Token(cl.value)
                R.GetType(operations,keywords)
                return R
            returned, value = statement.Execute(local_parser)
     
            if returned & RETURNING:
                cl = Token(value.value)
                cl.GetType(operations,keywords)
                return cl
            if returned & CONTINUE:
                continue

            idx += 1 
        return Token(0, NUMBER).copy()
