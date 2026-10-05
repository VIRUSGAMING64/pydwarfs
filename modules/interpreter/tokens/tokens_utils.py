from typing import TYPE_CHECKING

from modules.interpreter.statics import *

if TYPE_CHECKING:
    from modules.interpreter.tokens.token import Token

def IsOperator(tk: "Token"):
    return tk.name in operators


def is_unary(tk: "Token"):
    return tk.name in unarysops

def ValidLoop(line: Token):
    if line.subtokens[0].name != "while":
        return False

    return True

def ValidLabel(line: Token):
    if (line.subtokens[0].type & LABEL) == 0:
        return False
    if len(line.subtokens) != 1:
        return False
    return True

def validGoto(line):
    if line.type & LINE == 0:
        return False
    if len(line.subtokens) != 2:
        return False

    return line.subtokens[0].value == "goto"

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


def ValidFunctionStart(line : Token):
    if len(line.subtokens) < 4:
        return False
    if line.subtokens[0].name != "func":
            return False
    if line.subtokens[2].name != "(":
        return False
    if line.subtokens[-1].name != ")":
        return False
            
    return True
