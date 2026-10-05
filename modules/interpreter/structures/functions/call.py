
from modules.interpreter.tokens.token import Token, Parser
from modules.interpreter.statics import *
import modules.interpreter.tokens.tokens_utils as tk_utils
from modules.interpreter.exceptions import *
from modules.interpreter.structures.structure import *

class FuncCall(Structure):
    args: list[Token] = None
    def __init__(self, name, args, line):
        if not isinstance(args, list):
            raise Exception("args not is a list")
        self.type = FUNCCALL
        self.args = args
        self.name = name

    def __dict__(self):
        di = super().__dict__()
        del di["data"]
        del di["value"]
        del di["expr"]
        del di["subtokens"]
        di["args"] = []
        for a in self.args:
            t = []
            for i in a:
                t.append(i.__dict__()) 
            di["args"].append(t)  
        return di


"""
*Code extracted from https://github.com/VIRUSGAMING64/cryton2
*My first interpreter 

    def call(self, currline, args:list, mem:Memory):
        m_func = mem.query(currline.data["name"])
        while (m_func.type & FUNC) == 0:
            m_func = mem.query(m_func.data["name"])
            
        code = m_func.code      

        if len(m_func.args) != len(args):
            if debug.DEBUG:
                print(m_func.args, args)
            raise CallFuncException(currline)
        
        if code == BUILTIN:
            #* Aqui chequeo si la llamada a la funcion es de una builtin
            #* (funciones implementadas en python para el lang)
            name = m_func.name
            try:
                ret = in_builtin.__builtins_calls__[name](*args)
            except Exception as e:
                raise BuiltinException(e)
            if ret == None:
                ret = Token(ret, GetType(ret))
            return ret.copy()

        newmem = Memory() 
        #* Aqui se crea un nuevo memory  segment para esta llamada
        #* en el for se declaran en ese nuevo segmento las variables que se pasana como argumento
        for i,arg_name in enumerate(m_func.args):
            newmem.alloc_var(
                arg_name, args[i].copy(), False, False
            )
        
        #* en este for las variables globales se pasan por referencia a la siguiente llamada de funcion
        for addr in mem.mem:
            if mem.mem[addr].isglob == False:
                continue
            if newmem.mem.get(addr) != None:
                continue 
            newmem.mem[addr] = mem.mem[addr] #* Aqui lo que se hace es coger la referencia directa a las globales   
           
        code, ret = Evaluator(code, 0 , self.out, newmem, True).run()       
        if ret == None:
            ret = 0 #* defalut return value of function
            ret = Token(ret, GetType(ret))
        ret.type = GetType(ret.type)
        return ret.copy() 

    def callfuncs(self, toks, li):
        for i in range(len(toks.tokens)):
            if toks.tokens[i].type & FUNCCALL:
                args = []
                for arg in toks.tokens[i].data["args"]:
                    if arg == []:
                        continue
                    arg = self.evalTokens(arg, li)
                    args.append(arg)
                try:
                    toks.tokens[i] = self.call(toks.tokens[i], args, self.memory)
                except TypeError as e:
                    self.out["Errors"].append(f"Invalid argument type at line {toks.data.get("line", "unknow")}")
                    return 0

"""