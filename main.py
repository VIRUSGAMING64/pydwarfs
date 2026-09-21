from modules.game import *
from modules.interpreter import *
from gui.server.server import *
from threading import Thread
import json
import asyncio

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


def TestServer():
    path = "./gui/src"
    ser = Server("127.0.0.1", 1200, path)
    routes = Routes(path)
    ser.AddEndpoint("/", routes.hola)
    ser.AddEndpoint("/<path>", routes.getfile )
    print("starting webpage...")
    Thread(target= ser.Run,daemon=True).start()
    print("starting websocks...")
    wser = WebSockServer()
    asyncio.run(wser.RunWebsocks())

def TestServerCom():
    path = "./gui/src"
    ser = Server("127.0.0.1", 1200, path)
    routes = Routes(path)
    ser.AddEndpoint("/", routes.hola)
    ser.AddEndpoint("/<path>", routes.getfile )
    print("starting webpage...")
    Thread(target= ser.Run,daemon=True).start()
    print("starting websocks...")
    g = Game()
    g.LoadObjects()
    g.LoadTerrains()
    g.LoadMaps()
    wser = WebSockServer(g)
    asyncio.run(wser.RunWebsocks())


def InterTest():
    iner = Interpreter(open("codigotest.txt","r").read())
    for i in range(10):
        iner.Step()


TestAstBuild()
TestGameLoading()
#TestExprParser()
#TestServerCom()
InterTest()