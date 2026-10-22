#TODO

from modules.interpreter.statics import *

def RegisterTileProvider(provider):
    global tile_provider
    tile_provider = provider


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

def reproduce(memory, args):
    dx = args[0]
    dy = args[1]
    dam= args[2]



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