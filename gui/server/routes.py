import flask
import os

def get_mime_type(filename):
    mime_types = {
        '.css': 'text/css',
        '.svg': 'image/svg+xml',
        '.js': 'application/javascript',
        '.ts': 'application/javascript'
    }
    for ext, mime in mime_types.items():
        if filename.endswith(ext):
            return mime
    return None

class Routes:
    def __init__(self, path):
        self.base_path = path

    def hola(self):
        return self.getfile("index.html")

    def getfile(self,path):  
        path = os.path.join(self.base_path, path)
        try:
            with open(path) as file:
                return flask.Response(file.read(), mimetype=get_mime_type(path))
        except:
            return flask.Response("", status=404)