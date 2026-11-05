from modules.interpreter.lexer import *
from modules.interpreter.ast import *
from modules.interpreter.memory import *

def void():
    pass

class Interpreter:
    ast:AstBuilder = None
    line:int = 0
    memory: Memory = None

    def copy(self):
        iner = Interpreter()
        iner.memory = self.memory.copy()
        iner.line = self.line
        iner.ast = self.ast.copy() 
             
        iner.parser = Parser(iner.memory)
        return iner

    def __dict__(self):
        di = {
            "memory": self.memory.__dict__(),
            "line": self.line
        }
        return di

    def __init__(self, rawSrc="", filename = "__file__"):
        if rawSrc == "":
            if filename == "__file__": return 
            with open(filename, "r", encoding="utf-8") as f:
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
        lexed = Lexer(rawSrc)
        self.ast = AstBuilder(lexed.TokenizeSource())
        self.ast.ExtractStructures(memory=self.memory)
        for GotosLabel in self.ast.gotoslabels:
            if FindLabel(GotosLabel, self.ast.Ast) == -1:
                raise Exception("Semantic exceptions, label unknow")

        idx = FindLabel("start", self.ast.Ast)
        if idx == -1:
            raise Exception("Entry point unknow")

        #* En el pdf se dice q todo lo que esta antes de start:
        #* es un header por tanto no debe haber labels antes de start
        #* de todas formas start se busca usualmente
        tmp_loadeds = []
        for i in range(idx):
            li = self.ast.Ast[i]
            if li.type & FUNCTION:
                continue
            if len(li.subtokens) != 2:
                raise Exception(f"Invalid header at line [{li.line}]")        
            head = li.subtokens[0].name
            val = li.subtokens[1].value
            if not (head in attrs):
                raise Exception("Invalid header")  
            value = Token(val)
            value.GetType(operators, keywords)           
            self.memory.alloc(head, value)
            tmp_loadeds.append(head)
        #* Checking creatures attributes
        for attr in attrs:
            if not attr in tmp_loadeds:
                raise Exception(f"Creature with missing attribute [{attr}] error at file: [{filename}]")

        self.memory.alloc_const("x", Token(0,NUMBER))
        self.memory.alloc_const("y", Token(0,NUMBER))
        self.memory.alloc_const("NONE", Token(-1,NUMBER))
        self.memory.alloc_const("GROUND", Token(0,NUMBER))
        self.memory.alloc_const("OBJECT", Token(1,NUMBER))
        self.memory.alloc_const("ALLY", Token(2,NUMBER))
        self.memory.alloc_const("ENEMY", Token(3,NUMBER))
        self.line = idx
        self.parser = Parser(self.memory)


    def query(self, attr):
        return self.memory.query(attr)

    def Step(self):
        if self.line >= len(self.ast.Ast):
            return False

        ip = self.ast.Ast[self.line]
        #*Aqui voy a ignorar las label
        if ip.type & LABEL:
            self.line += 1
            return self.Step()
            
        code, out = ip.Execute(self.parser)
        if code & FINDING:
            self.line = FindLabel(out,self.ast.Ast)
            if self.line == -1:
                err = str(f"Label {out} no encontrado")
                raise Exception(err)
            return True
        
        elif code & CONTINUE:
            self.line -= 1
        
        self.line+=1
        return True
        
    def ReduceLifespan(self):
        self.memory.alloc_const("lifespan", Token(self.memory.query("lifespan").value - 1, NUMBER))

    def Lifespan(self):
        return self.memory.query("lifespan")
    
    def Vision(self):
        return self.memory.query("vision")
    
    def Faction(self):
        return self.memory.query("faction")
    
    def Health(self):
        return self.memory.query("health")