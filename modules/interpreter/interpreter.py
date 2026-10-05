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

    def __dict__(self):
        di = {
            "memory": self.memory.__dict__(),
            "line": self.line
        }
        return di

    def __init__(self, rawSrc="", filename = "__file__"):
        if rawSrc == "":
            with open(filename,"rb") as f:
                rawSrc = f.read()

        self.memory = Memory()
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
        self.ast.ExtractStructures(memory=self.memory)
       
        idx = self.FindLabel("start", self.ast.Ast)
        if idx == -1:
            raise Exception("Entry point unknow")


        #* Initializing attrubutes
        for attr in attrs:
            self.__setattr__(attr, None)

        #* En el pdf se dice q todo lo que esta antes de start:
        #* es un header por tanto no debe haber labels antes de start
        #* de todas formas start se busca usualmente

        for i in range(idx):
            li = self.ast.Ast[i]
            if len(li.subtokens) != 2:
                raise Exception(f"Invalid header at line [{li.line}]")        
            head = li.subtokens[0].name
            val = li.subtokens[1].value
            if not (head in attrs):
                raise Exception("Invalid header")        
            self.__setattr__(head, val)  
            value = Token(val)
            value.GetType(operators, keywords)              
            self.memory.alloc(head, value)

        #* Checking creatures attributes
        for attr in attrs:
            if self.__getattribute__(attr)==None:
                raise Exception(f"Creature with missing attribute [{attr}] error at file: [{filename}]")

        self.alloc("x", Token(0,NUMBER))
        self.alloc("y", Token(0,NUMBER))

        self.line = idx
        self.parser = Parser(self.memory)
                
    def query(self, attr):
        return self.memory.query(attr)

    def alloc(self, attr, val):
        self.memory.alloc(attr,val)

    def FindLabel(self, label, lines)-> int:
        for i, elem in enumerate(lines):
            if elem.type&LABEL:
                if elem.type == LABEL and elem.name == label:
                    return i
            elif label != "start": #* Aqui se evita que start: este dentro de algo
                pos = self.FindLabel(label, elem.subtokens)
                if pos != -1:
                    elem.ip = pos
                    return i
        return -1

    def Step(self):
        if self.line >= len(self.ast.Ast):
            return False

        ip = self.ast.Ast[self.line]
        code, out = ip.Execute(self.parser)
        if code & FINDING:
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