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
        lexed = Lexer(rawSrc, errors)
        logging.debug(errors["Errors"])
        self.ast = AstBuilder(lexed.TokenizeSource())
        self.ast.ExtractStructures()
        self.memory = Memory()

    def FindLabel(self, label, lines)-> int:
        for i, elem in enumerate(lines):
            if elem.type&LINE:
                if elem.subtokens[0].type == LABEL and elem.subtokens[0].name == label:
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
        print("Executed: ",self.line, type(ip))
        print(ip.name)
        print("-------")
        code, out = ip.Execute(parser)
        if code == FINDING:
            p = self.FindLabel(out,self.ast.Ast)
            self.line = p
            print("Label en: ", p)
            if p == -1:
                err = str(f"Label {out} no encontrado")
                raise Exception(err)
            return True
        elif code == CONTINUE:
            self.line -= 1
        print("line: ", self.line, "evaluated")
        self.line+=1
        return True