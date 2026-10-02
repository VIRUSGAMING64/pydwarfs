from modules.interpreter.structures import *


def ToksCompression(tokens: list[Token]):
    s = ""
    for i in tokens:
        s += i.name + " "
    s=s.removesuffix(" ")
    tok = Token(s)
    tok.line = LINE
    tok.subtokens = [tk.copy() for tk in tokens]
    return tok

class AstBuilder:
    Ast:list[Token|Loop|Condition] = None
    labels:dict = None
    def __init__(self, code: list[Token]):
        self.Ast = code
        self.labels = {}

    def __json__(self):
        return [t.__dict__() for t in self.Ast]

    def ExtractStructures(self, start=0, toks =None):
        
        i = start
        Ast = []
        if toks == None:
            toks = self.Ast

        while i < len(toks):
            subtok = toks[i]
            if tk_utils.ValidLabel(subtok):
                li = Label(subtok)
                n = self.labels.get(li.name, 0)+1
                if n >= 2:
                    raise Exception(f"Two labels with same name: {li.name}")
                self.labels[li.name] = n
                Ast.append(li)
                i += 1
                continue
            elif tk_utils.ValidLoop(subtok):
                end , structures = self.ExtractStructures(i + 1, toks)
                lo = Loop([toks[i]]  + structures)
                Ast.append(lo)
                i = end+1
            elif tk_utils.ValidCondition(subtok):
                end , structures = self.ExtractStructures(i + 1, toks)
                cond = Condition([toks[i]]  + structures)
                Ast.append(cond)
                i = end+1
            elif tk_utils.ValidGotoCondition(subtok):                  
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
                    lie = Goto(lie.subtokens[1])

                Ast.append(
                    lie
                )
                i += 1

        if start == 0:
            self.Ast = Ast
            return
        
        raise Exception(f"Not closed strucure starting at line [{start}]")