from flask import Flask
import websockets
import os
import json
from gui.server.routes import *
import time
from modules.game import *


class CommunicationStatus:
    STEP = 1
    CLOSE = 2
    CONTINUE = 3
    SIGKILL = 4
    SHOW = 5
    ADD = 6

class WebSockServer:
    websock = None 
    game = None
    def __init__(self, game: Game):
        self.game = game

    async def RunWebsocks(self):
        self.websock = await websockets.serve(self.OnConnect, "127.0.0.1", port=9090)
        print("Server started")
        await self.websock.serve_forever()

    async def OnConnect(self, cli: websockets.ServerConnection):
        print("hi: ", cli.latency)
        while cli.state == websockets.State.OPEN:
            cli_data = await cli.recv()
            out = self.Action(cli_data)
            await cli.send(out)

    def AddEntity(self,obj):
        obj: dict = json.loads(obj)
        name=obj.get("name")
        x = obj.get("x")
        y=obj.get("y")
        if None in [name, x, y]:
            raise Exception("un error ahi para despues")
            #! deuda tecnica

        for tmp_c in self.game.Creatures:
            c_name= tmp_c.memory.addrs.get("creature").name 
            if c_name == name:
                c = tmp_c.copy()
                c.memory.addrs["x"].value = int(x)
                c.memory.addrs["y"].value = int(y)
                self.game.RunningCreatures.append(c)

    def Action(self, RawData: str):
        try:
            print(RawData)
            data = RawData.split("__DATA__")
            code = data[0]
            data = data[1]
            if not code.isnumeric():
                return "invalid data" #* Aqui hay que hacer algo mejor para esto
            code = int(code)
            result = "" 
            if code == CommunicationStatus.STEP:
                self.game.Step()
            elif code == CommunicationStatus.SHOW:
                result = self.game.__dict__()
                result = json.dumps(result)
            elif code == CommunicationStatus.SIGKILL:
                result = "KILLED"
                self.game.kill()
            elif code == CommunicationStatus.ADD:
                self.AddEntity(data)
                result = self.game.__dict__()
                result = json.dumps(result)
        
            return result
        
        except Exception as e:
            print(e)
            exit(0)
class Server:
    app:Flask = None
    def __init__(self, host:str, port:int, path:str):        
        self.app = Flask("app")
        self.host = host
        self.port = port
        self.path = path
        self.clients = []
        if path.startswith("./"):
            path = path.removeprefix("./")
            self.path = os.path.join(os.getcwd(), path)

    
    def AddEndpoint(self, endpoint, callable,arg = []):
       self.app.add_url_rule(endpoint, view_func=callable,)


    def Run(self):
        self.app.run(self.host, self.port)
