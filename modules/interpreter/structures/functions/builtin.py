#TODO

#* Aqui van las functions del juego para parsear


def move(memory, args):
    memory.alloc("x", args[0])
    memory.alloc("y", args[1])


def say(memory, args):
    cosa = args[0]
    print(cosa.value)

builtins = [
    "move",
    "say"
]


builtinfuncs = {
    "move": move,
    "say": say
}

argslens = {
    "move": 2,
    "say": 1
}