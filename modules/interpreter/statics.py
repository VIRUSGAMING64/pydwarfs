#* Types
NIL = 0
NUMBER = 1
STRING = 2
POINTER = 4
OPERATOR = 8
VARIABLE = 16
KEYWORD = 32
LINE = 64
CODE = 128
COMMENT = 256
CONDITION = 512
LOOP = 1024
LABEL = 2048
GOTO = 4096
FUNCTION = 8192


P0 = [
    "==",
    "<=>",
    "=>",
    "!=",
    "<=",
    ">=",
    "<",
    ">",
    "<<",
    ">>",
    "="
]

P1 = [    
    "+",
    "-",
]

P2 = [
    "%",
    "*",
    "/",
    "!",
    "and",
    "or",
    "xor"
]

P3 = [
    "**",
]

operators =  [
    "=",
    ")",
    "(",
    "]",
    "[",
    ",",
    "#"
]

unarysops = [
    "!", "-", "+"
]

operators += P0 + P1 + P2 + P3

keywords = [
    "goto",
    "if",
    "func",
    "var",
    "for",
    "end"

]

maths = {
    "=":"=",
    "<":"=",
    ">":"=",
    "=": ">",
    ">": ">",
    "<": "<",
    "*": "*"
}
