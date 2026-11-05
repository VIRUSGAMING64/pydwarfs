from modules.game import *
from modules.interpreter import *
from gui.server.server import *
from threading import Thread
import json
import asyncio
import sys


def TestServerCom():
    path = "./src"
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
    g.LoadCreatures()
    GenericBuiltinFunctions.game = g
    wser = WebSockServer(g)
    print("websockets starteds")
    asyncio.run(wser.RunWebsocks())

def InterTest():
    iner = Interpreter(open("codigotest.txt","r").read())
    di = iner.ast.__json__()
    s = json.dumps(di, indent="   ")
    open("ast.json", "w").write(s)
    g = Game()
    GenericBuiltinFunctions.game = g
    g.RunningCreatures.append(iner.copy())
    for i in range(10**6):
        p = g.Step()
        if not p:
            break

if "--web" in sys.argv:
    TestServerCom()
else:
    InterTest()

