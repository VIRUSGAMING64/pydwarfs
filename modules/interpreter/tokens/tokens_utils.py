from modules.interpreter.tokens.token import *

def ValidLoop(tk: Token):
    if tk.name != "while":
        return False

    return True

def ValidCondition(tk : Token):
    if tk.name != "if":
        return False

    return True

def IsOperator(tk : Token):
    return True if tk.name in operators else False    

def is_unary(tk : Token):
    return True if tk.name in unarysops else False


def getPrio(value):
    if value.data.get("neg", False):
        return 3
    op = value.value
    if op in P0:
        return 0
    if op in P1:
        return 1
    if op in P2:
        return 2
    if op in P3:
        return 3
    return -1

def asign(a, b, mem):
   pass #TODO
    
def UnaryOP(a,op):
    return una[op.value](a)

operations = {
    "+":lambda a, b: a.value + b.value,
    "-":lambda a, b: a.value - b.value,
    "*":lambda a, b: a.value * b.value,
    "/":lambda a, b: a.value // b.value,
    "<<":lambda a,b: a.value << b.value,
    ">>":lambda a,b: a.value >> b.value,
    "**":lambda a,b: a.value ** b.value,
    "!":lambda a:  not a.value,
    "|":lambda a, b: a.value | b.value,
    "^":lambda a, b: a.value ^ b.value,
    "&":lambda a, b: a.value & b.value,
    "!=": lambda a, b: a.value != b.value,
    "==": lambda a, b: a.value == b.value,
    "<=": lambda a, b: a.value <= b.value,
    ">=": lambda a, b: a.value >= b.value,
    "<": lambda a, b: a.value < b.value,
    ">": lambda a, b: a.value > b.value,
    "%": lambda a, b: a.value % b.value,
    "=>": lambda a,b: (not a.value) | b.value,
    "<=>": lambda a,b: ((not a.value) | b.value) ^ ((not b.value) | a.value),
    "=": asign
}
def isdelim(s):
    return True if s == " " else False

def _not(a):
    return not a.value

def neg(a):
    return  -a.value

def plus(a):
    return a.value


una = {
    "-": neg,
    "+": plus,
    "!": _not
}


def process_op(b,a,op, mem):
    if op.value == "=":
        return operations[op.value](a,b,mem)
    return operations[op.value](a,b)
