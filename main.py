from modules.interpreter import *

import json

di = []

tokens = Lexer(open("codigotest.txt","r").read(10000000), {}).TokenizeSource()
i = 0
while i < len(tokens):
    tk = tokens[i]
    if tk_utils.ValidLoop(tk.subtokens[0]):
        print("here")
        tk = Loop(tokens[i : ], Token("end")) 
        e=tk.Exctract()
        i += e
    i += 1
    di.append(tk.__dict__())  


s = json.dumps(di, indent="   ")
open("ast.dat", "w").write(s)
