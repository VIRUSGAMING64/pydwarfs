#TODO

from modules.interpreter.statics import *
#* Aqui van las functions del juego para parsear


def move(memory, args):
    memory.alloc_const("x", args[0])
    memory.alloc_const("y", args[1])


def say(memory, args):
    cosa = args[0]
    print(cosa.value)


def wait(memory ,args):
    num = args[0]
    if (num.type & NUMBER ) == 0:
        raise Exception("un error para sergio")

builtins = [
    "move",
    "say",
    "wait"
]


builtinfuncs = {
    "move": move,
    "say": say,
    "wait": wait
}

argslens = {
    "move": 2,
    "say": 1,
    "wait": 1
}