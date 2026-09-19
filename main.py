from modules.game import *
from modules.interpreter import *
import json

def TestAstBuild():
    di = []

    tokens = Lexer(open("codigotest.txt","r").read(10000000), {}).TokenizeSource()
    ast = AstBuilder(tokens)
    ast.ExtractLoops()
    ast.ExtractConditions()
    di = ast.__json__()
    s = json.dumps(di, indent="   ")
    open("ast.dat", "w").write(s)


def TestGameLoading():
    g = Game()
    g.LoadTerrains()
    g.LoadObjects()
    g.LoadMaps()
    open("gamedump.txt","w").write((json.dumps(g.__dict__(), indent="    ")))

def TestExprParser():
    tokens = Lexer(open("codigotest.txt","r").read(10000000), {}).TokenizeSource()
    ast = AstBuilder(tokens)
    ast.ExtractLoops()
    ast.ExtractConditions()
    int = Parser()
    for line in ast.Ast:
        res = int.EvalExpr(line.subtokens)
        #print(res.__dict__())

TestExprParser()
TestAstBuild()
TestGameLoading()