from modules.interpreter import *

import json

di = [tk.__dict__() for tk in Lexer(open("codigotest.txt","r").read(10000000), {}).TokenizeSource()]
s = json.dumps(di, indent="   ")
open("ast.dat", "w").write(s)
