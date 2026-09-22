from modules.interpreter.tokens.token import *

def ValidLoop(line: Token):
    if line.subtokens[0].name != "while":
        return False

    return True

def ValidCondition(line : Token):
    if line.subtokens[0].name != "if":
        return False
    for i in line.subtokens:
        if i.value == "goto":
            return False
    return True

def ValidGotoCondition(line : Token):
    if line.subtokens[0].name != "if":
        return False
    for i in line.subtokens:
        if i.value == "goto":
            return True
    return False

