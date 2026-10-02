from modules.interpreter.lexer import *
from modules.interpreter.ast import *
from modules.interpreter.parser.parser import *
import logging


logging.basicConfig(level=logging.DEBUG)

def void():
    pass

class Interpreter:
    ast:AstBuilder = None
    line:int = 0
    memory: Memory = None

    def __init__(self, rawSrc):
        errors = {}
        attrs = [
            "creature", 
            "faction", 
            "health", 
            "vision", 
            "lifespan"
        ]
        lexed = Lexer(rawSrc, errors)
        logging.debug(errors["Errors"])
        self.ast = AstBuilder(lexed.TokenizeSource())
        self.ast.ExtractStructures()
        self.memory = Memory()
        idx = self.FindLabel("start", self.ast.Ast)
        if idx == -1:
            raise Exception("Entry point unknow")

        for i in range(idx):
            li = self.ast.Ast[i]
            if len(li.subtokens) != 2:
                raise Exception("Invalid header")        
            head = li.subtokens[0].name
            val = li.subtokens[1].value
            if not (head in attrs):
                raise Exception("Invalid header")        
            self.__setattr__(head, val)

        self.line = idx
#        print("iniciacion:",self.creature)

    def FindLabel(self, label, lines)-> int:
        for i, elem in enumerate(lines):
            if elem.type&LABEL:
                if elem.type == LABEL and elem.name == label:
                    return i
            else:
                pos = self.FindLabel(label, elem.subtokens)
                if pos != -1:
                    elem.ip = pos
                    return i
        return -1

    def Step(self):
        if self.line >= len(self.ast.Ast):
            return False

        parser = Parser(self.memory)
        ip = self.ast.Ast[self.line]
        code, out = ip.Execute(parser)
        if code == FINDING:
            p = self.FindLabel(out,self.ast.Ast)
            self.line = p
            if p == -1:
                err = str(f"Label {out} no encontrado")
                raise Exception(err)
            return True
        elif code == CONTINUE:
            self.line -= 1
        self.line+=1
        return True