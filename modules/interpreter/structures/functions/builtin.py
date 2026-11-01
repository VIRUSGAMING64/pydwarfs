from modules.interpreter.statics import *
builtins = [
    "move",
    "say",
    "wait"
]



class Builtins:
    WaitTempData:dict = None
    game: "Game" = None
    def __init__(self, game = None):
        self.WaitTempData={}
        self.builtinfuncs = {
            "move": self.move,
            "say": self.say,
            "wait": self.wait
        }

        self.argslens = {
            "move": 3,
            "say": 1,
            "wait": 1
        }
        self.game = game

    def move(self,memory, args):
        dx = args[0].value
        dy = args[1].value
        speed = args[2].value
        for _ in range(speed):
            xpos = memory.query("x") 
            xpos.value += dx
            ypos = memory.query("y") 
            ypos.value += dy
            obj = self.game.GetObjectAt(xpos.value, ypos.value)
            ent = self.game.GetEntityAt(xpos.value, ypos.value)
            if (obj == None) and (ent == None):
                memory.alloc_const("x", xpos)
                memory.alloc_const("y", ypos)
            else: 
                print(obj, ent)
                break
        
        return NORMAL, None


    def roar(self, memory, args):
        self.game.PostRoar(args[0])

    def say(self,memory, args):
        cosa = args[0]
        print(cosa.value)
        return NORMAL, None

    def wait(self,memory ,args):
        num = args[0]
        if self.WaitTempData.get(memory.id, -1) == -1:
            self.WaitTempData[memory.id] = 0
        self.WaitTempData[memory.id] += 1
        if (num.type & NUMBER ) == 0:
            raise Exception("un error para sergio")

        if self.WaitTempData[memory.id] == num.value:
            return NORMAL, None
        return CONTINUE, None

    def reproduce(self,memory, args):
        dx = args[0]
        dy = args[1]
        dam= args[2]
        return NORMAL, None



GenericBuiltinFunctions = Builtins()