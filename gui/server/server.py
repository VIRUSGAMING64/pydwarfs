from flask import Flask
import websockets
import os
import json
from gui.server.routes import *
import time
from modules.game import *

MAX_LOAD_COUNT = 100


class CommunicationStatus:
    STEP = 1
    CLOSE = 2
    CONTINUE = 3
    SIGKILL = 4
    ADD = 6
    LOAD_LOGS = 7
    LOAD_MAP = 15
    FRAME = 8

class WebSockServer:
    websock = None 
    game = None
    def __init__(self, game: Game):
        self.game = game
        self.CurrMap = None

    async def RunWebsocks(self):
        self.websock = await websockets.serve(self.OnConnect, "127.0.0.1", port=9090)
        print("Server started")
        await self.websock.serve_forever()

    async def OnConnect(self, cli: websockets.ServerConnection):
        print("hi: ", cli.latency)
        while cli.state == websockets.State.OPEN:
            try:
                cli_data = await cli.recv()
                out = self.Action(cli_data)
                await cli.send(out)
            except Exception as e:
                print(e)

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

    def Creaturelogs(self):
        logs = self.game.LoadLogs()
        r_logs = logs.copy()
        r_logs.reverse()
        r_logs = r_logs[:MAX_LOAD_COUNT]
        t_logs = []
        for c,log,isroar in r_logs:
            data = {"x": c.X().value, "y": c.Y().value, "data": log, "roar": isroar}
            t_logs.append(data)
        
        dic = {
            "isloadlogs": True,
            "cnt": len(t_logs),
            "logs": t_logs
        }
        return dic

    def Frame(self, data: str):
        payload = json.loads(data) if data else {}
        if payload.get("advance", False):
            self.game.Step()

        logs = self.game.LoadLogs()
        cursor = max(0, min(int(payload.get("logCursor", 0)), len(logs)))
        if cursor == 0:
            cursor = max(0, len(logs) - MAX_LOAD_COUNT)
        new_logs = []
        for c, log, isroar in logs[cursor:]:
            new_logs.append({"x": c.X().value, "y": c.Y().value, "data": log, "roar": isroar})

        result = self.game.__dict__()
        result["isloadlogs"] = False
        result["logs"] = new_logs
        result["logCursor"] = len(logs)
        return json.dumps(result)

    def SelectMap(self,name:str):
        if name == None:
            raise Exception("un error ahi para despues")
            #! deuda tecnica
        try:
            name = json.loads(name)
        except json.JSONDecodeError:
            name = name.removeprefix("'").removesuffix("\"")
        for map in self.game.Maps:

            if map.Name == name:
                self.game.SelectMap(map)
                return

    def Action(self, RawData: str):
        try:
            data = RawData.split("__DATA__")
            code = data[0]
            data = data[1]
            if not code.isnumeric():
                return "invalid data" #* Aqui hay que hacer algo mejor para esto
            code = int(code)
            result = "" 
            if code == CommunicationStatus.STEP:
                self.game.Step()
            elif code == CommunicationStatus.LOAD_MAP:
                self.SelectMap(data)
            elif code == CommunicationStatus.SIGKILL:
                result = "KILLED"
                self.game.kill()
            elif code == CommunicationStatus.LOAD_LOGS:
                result = self.Creaturelogs() #* Returns a json with logs {cnt, logs}
                result = json.dumps(result)
            elif code == CommunicationStatus.FRAME:
                result = self.Frame(data)
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
       self.app.add_url_rule(endpoint, view_func=callable)


    def Run(self):
        self.app.run(self.host, self.port)
