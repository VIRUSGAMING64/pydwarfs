from flask import Flask
import websockets
import os
import json
from gui.server.routes import *
import time


class WebSockServer:
    websock = None 
    game = None
    def __init__(self, game):
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

    def Action(self, RawData):
        data = "unknowaction"
        if RawData == "STEP":
            self.game.step()
        elif RawData == "SHOW":
            data = self.game.__dict__()
            data = json.dumps(data)
        elif RawData == "SIGKILL":
            data = "KILLED"
            self.game.kill()
        return data

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
