from modules.interpreter.structures import *
from modules.interpreter.structures.functions.builtin import builtins
class AstBuilder:
    Ast:list[Token|Loop|Condition] 
    labels:dict 

    def __init__(self, code: list[Token]):
        self.Ast = code
        self.labels = {}
        self.prefuncs = {}
        self.builtin = {}
        for i in builtins:
            self.builtin[i] = True
            self.prefuncs[i] = i
        self.funcs = []

    def funcat(self, i , tokens):
        """
        Se recorre la expression y se va haciendo splists segun aparezcan ","
        hasta llegar al cierre de la funcion
        """
        opens = 1
        args = []
        arg = []
        for j in range(i+2, len(tokens)):
            if tokens[j].value == "(":
                opens += 1
                arg.append(tokens[j])
            elif tokens[j].value == ",":
                if opens == 1:    
                    args.append(arg)
                    if len(arg) == 0:
                        raise CallFuncException("Invalid argument")
                    arg = []
                else:
                    arg.append(tokens[j])
            elif tokens[j].value == ")":
                opens -= 1
                arg.append(tokens[j])
            else:
                arg.append(tokens[j])

            if opens == 0:
                arg.pop()
                if len(arg) > 0:
                    args.append(arg)
                return j,args
        
        raise CallFuncException("Not closed function call !!")#* La cantidad de "(" > ")" entonces faltan ) para algunos ( 
    

    def extract_funcs_call(self,tokens, mem:Memory):
        for i in range(len(tokens)):
            if i + 1 >= len(tokens):
                break
            if (tokens[i].type & VARIABLE) and tokens[i + 1].value == "(":
                name = tokens[i].name
                fu = self.prefuncs.get(name,None)

                if fu == None:
                    raise MissingVariable(name)
                
                eofc,args = self.funcat(i,tokens)
                for a in args:
                    self.extract_funcs_call(a, mem)
                
                func = FuncCall(name,args, tokens[0].line) 
                func.isbuiltin = self.builtin.get(name, False)
                del tokens[i : eofc + 1]
                tokens.insert(i, func)


    def __json__(self):
        return [t.__dict__() for t in self.Ast]


    def ExtractStructures(self, start=0, toks = None, memory:Memory = None, infunc = False):
        
        i = start
        Ast = []
        if toks == None:
            toks = self.Ast

        while i < len(toks):
            subtok = toks[i]

            if not tk_utils.ValidFunctionStart(subtok):
                self.extract_funcs_call(subtok.subtokens, memory)

            if tk_utils.ValidLabel(subtok):
                if infunc:
                    raise SintaxisException("Can't create label into function")
                li = Label(subtok)
                n = self.labels.get(li.name, 0)+1
                if n >= 2:
                    raise Exception(f"Two labels with same name: {li.name}")
                self.labels[li.name] = n
                Ast.append(li)
                i += 1
                continue

            elif tk_utils.ValidFunctionStart(subtok):
                if start != 0:
                    raise Exception("Not declare functions in structures")

                declaration = subtok.copy()
                name = declaration.subtokens[1].name
                if self.prefuncs.get(name, None) != None:
                    raise Exception("Functions with same name are detected")
                self.prefuncs[name] = name

                end , structures = self.ExtractStructures(i + 1, toks, memory, infunc|True)
                tfunc = Function([declaration.copy()] + structures)
                memory.alloc(tfunc.name, tfunc)

                i = end + 1
                Ast.append(tfunc)
                
            elif tk_utils.ValidLoop(subtok):
                end , structures = self.ExtractStructures(i + 1, toks, memory,infunc)
                lo = Loop([toks[i]]  + structures)
                Ast.append(lo)
                i = end+1
            elif tk_utils.ValidCondition(subtok):
                end , structures = self.ExtractStructures(i + 1, toks, memory,infunc)
                cond = Condition([toks[i]]  + structures)
                Ast.append(cond)
                i = end+1
            elif tk_utils.ValidGotoCondition(subtok):   
                if infunc:
                    raise SintaxisException("Can't create goto into function")               
                for j,elem in enumerate(toks[i].subtokens):
                    if elem.name == "goto":
                        expr = toks[i].subtokens[0:j]
                        subtokens = toks[i].subtokens[j : ]
                        cond = Condition([
                            ToksCompression(expr),
                            ToksCompression(subtokens)
                        ])     
                        lie = SingleLine([cond.subtokens[0]] + cond.subtokens[0].subtokens)
                        if tk_utils.validGoto(lie):
                            lie = Goto(lie.subtokens[1])
                        cond.subtokens[0] = lie
                        Ast.append(cond)
                        i += 1
                        break
                continue
                    
            elif toks[i].value == "end":
                if start == 0:
                    self.Ast = Ast
                    return
                return i, Ast
            else:
                lie = SingleLine([toks[i]]  + toks[i].subtokens)
                if lie.subtokens[len(lie.subtokens ) - 1].type & COMMENT:
                    lie.subtokens.pop()
                if len(lie.subtokens) == 0:
                    i += 1
                    continue  
                if tk_utils.validGoto(lie):
                    if infunc:
                        raise SintaxisException("Can't create goto into function")               
                    lie = Goto(lie.subtokens[1])

                Ast.append(
                    lie
                )
                i += 1

        if start == 0:
            self.Ast = Ast
            return
        
        raise Exception(f"Not closed strucure starting at line [{start}]")