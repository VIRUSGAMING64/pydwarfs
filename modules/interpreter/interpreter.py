from modules.interpreter.lexer import *
from modules.interpreter.ast import *
from modules.interpreter.parser.parser import *
import logging


logging.basicConfig(level=logging.DEBUG)

class Interpreter:
    ast:AstBuilder = None
    line:int = 0

    def __init__(self, rawSrc):
        errors = {}
        lexed = Lexer(rawSrc, errors)
        logging.debug(errors["Errors"])
        self.ast = AstBuilder(lexed.TokenizeSource())
        self.ast.ExtractStructures()

    def Step(self):
        if self.line >= len(self.ast.Ast):
            return False

        parser = Parser()
        self.ast.Ast[self.line].Execute(parser)
        print("line: ", self.line, "evaluated")
        self.line+=1