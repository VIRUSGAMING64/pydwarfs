from modules.interpreter.tokens.token import *

def ValidLoop(tk: Token):
    if tk.name != "while":
        return False

    return True

def ValidCondition(tk : Token):
    if tk.name != "if":
        return False

    return True
