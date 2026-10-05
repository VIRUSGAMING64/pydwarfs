
from modules.interpreter.statics import *

from modules.interpreter.tokens.tokens_utils import IsOperator, is_unary
from modules.interpreter.tokens.token import *
from modules.interpreter.memory import *

def getPrio(value):
    if value.data.get("neg", False):
        return 3
    op = value.name
    if op in P0:
        return 0
    if op in P1:
        return 1
    if op in P2:
        return 2
    if op in P3:
        return 3
    return -1

def asign(a:"Token", b:"Token", mem: Memory):
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