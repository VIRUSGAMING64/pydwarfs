import flask 
import os
from gui.server.routes import *

class Server:
    app:flask.Flask = None
    def __init__(self, host:str, port:int, path:str):        
        self.app = flask.Flask("app")
        self.host = host
        self.port = port
        self.path = path
        if path.startswith("./"):
            path = path.removeprefix("./")
            self.path = os.path.join(os.getcwd(), path)

    def AddEndpoint(self, endpoint, callable,arg = []):
       self.app.add_url_rule(endpoint, view_func=callable,)

    def Run(self):
        self.app.run(self.host, self.port)


