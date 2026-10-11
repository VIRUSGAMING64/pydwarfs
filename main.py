from modules.game import *
from modules.interpreter import *
from gui.server.server import *
from threading import Thread
import json
import asyncio
import sys
sys.setrecursionlimit(2**30)

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
    for i in range(200):
        g.Step()
    wser = WebSockServer(g)
    asyncio.run(wser.RunWebsocks())


def InterTest():
    iner = Interpreter(open("codigotest.txt","r").read())
    di = iner.ast.__json__()
    s = json.dumps(di, indent="   ")
    open("ast.json", "w").write(s)
    while iner.Step():
        pass

    for i in iner.memory.addrs:
        print(i,":",iner.memory.addrs[i].value)

InterTest()
#TestServerCom()
