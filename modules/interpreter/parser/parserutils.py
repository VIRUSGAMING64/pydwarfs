
from modules.interpreter.statics import *

from modules.interpreter.tokens.tokens_utils import IsOperator, is_unary

def getPrio(value):
    if value.data.get("neg", False):
        return 5
    op = value.value
    if op == "or":
        return 0
    if op == "and":
        return 1
    if op in ("==", "!=", "<", "<=", ">", ">=", "=>", "<=>"):
        return 2
    if op in ("+", "-"):
        return 3
    if op in ("<<", ">>", "%", "*", "/"):
        return 4
    if op in ("**", "!"):
        return 5
    if op == "=":
        return -1
    return -1

def asign(a, b, mem):
    a.value = b.value
    mem.alloc(a.name, a)
   
    
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
    "or":lambda a, b: a.value | b.value,
    "xor":lambda a, b: a.value ^ b.value,
    "and":lambda a, b: a.value & b.value,
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