from modules.interpreter.statics import *
import uuid
from modules.interpreter.exceptions import *
from modules.interpreter.utils import OnlyBitmask

builtins = [
    "move",
    "say",
    "wait",
    "reproduce",
    "kill",
    "see"
]

class Builtins:
    WaitTempData:dict = None
    game: "Game" = None
    def __init__(self, game = None):
        self.WaitTempData={}
        self.builtinfuncs = {
            "move": self.move,
            "say": self.say,
            "wait": self.wait,
            "kill": self.kill,
            "reproduce": self.reproduce,
            "see": self.see
        }

        self.argslens = {
            "move": 3,
            "say": 1,
            "wait": 1,
            "reproduce": 3,
            "kill": 0,
            "see": 2
        }
        self.game = game

    def kill(self, memory, args):
        v=memory.query("health").copy()
        v.value = 0
        memory.alloc_const("health", v)
        return NORMAL, None

    def move(self,memory, args):
        dx = args[0].value
        dy = args[1].value
        speed = args[2].value
        if (dx not in (-1, 0, 1) or dy not in (-1, 0, 1) or
            (dx == 0 and dy == 0) or speed <= 0):
            raise FuncCallException("move direction must be between -1 and 1")

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
                break
        
        return NORMAL, None


    def roar(self, memory, args):
        self.game.PostRoar(args[0])

    def say(self,memory, args):
        cosa = args[0]
        print(cosa.value)
        #! Aqui falta hacer una notificacion en la gui
        return NORMAL, None

    def see(self, memory, args):

        for num in args:
            if not OnlyBitmask(num.type , [NUMBER,VARIABLE] ):
                raise FuncCallException("see arguments must be numbers")

        target_x, target_y = (arg.value for arg in args)
        current_x = memory.query("x").value
        current_y = memory.query("y").value
        vision = memory.query("vision").value

        distance = max(abs(target_x - current_x), abs(target_y - current_y))
        if distance > vision:
            return NORMAL, memory.query("NONE").value

        if self.game is None or not self.game.IsInsideMap(target_x, target_y):
            return NORMAL, memory.query("OBJECT").value

        entity = self.game.GetEntityAt(target_x, target_y)
        if entity is not None:
            if entity.memory.id == memory.id or (
                entity.Faction().value == memory.query("faction").value
            ):
                return NORMAL, memory.query("ALLY").value
            return NORMAL, memory.query("ENEMY").value

        if self.game.GetObjectAt(target_x, target_y) is not None:
            return NORMAL, memory.query("OBJECT").value

        return NORMAL, memory.query("GROUND").value

    def wait(self,memory ,args):
        num = args[0]

        if not OnlyBitmask(num.type , [NUMBER,VARIABLE] ):
            raise FuncCallException("Wait arguments must be numbers")
                    
        if self.WaitTempData.get(memory.id, -1) == -1:
            self.WaitTempData[memory.id] = 0
        self.WaitTempData[memory.id] += 1
        

        if self.WaitTempData[memory.id] == num.value:
            return NORMAL, None
        return CONTINUE, None

    def reproduce(self,memory, args):
        #! Aqui hay un bug y es que las cosas no pueden estar en el setattr
        for num in args:
            if not OnlyBitmask(num.type , [NUMBER,VARIABLE] ):
                raise FuncCallException("reproduce arguments must be numbers")

        dx, dy, health = [arg.value for arg in args]
        if (dx not in (-1, 0, 1) or dy not in (-1, 0, 1) or
            (dx == 0 and dy == 0) or health <= 0):
            raise FuncCallException("reproduce direction must be between -1 and 1")

        parent = None
        for creature in self.game.RunningCreatures:
            if creature.memory.id == memory.id:
                parent = creature
                break

        if parent == None:
            return NORMAL, None

        child_x = memory.query("x").value + dx
        child_y = memory.query("y").value + dy
        if (self.game.GetObjectAt(child_x, child_y) is not None or
                self.game.GetEntityAt(child_x, child_y) is not None):
            return NORMAL, None

        child = parent.copy()
        child.line = next(
            index for index, instruction in enumerate(child.ast.Ast)
            if instruction.type & LABEL and instruction.name == "start"
        )
        for name, value in list(child.memory.addrs.items()):
            if (name not in {"creature", "faction", "health", "vision", "lifespan"}
                    and name not in child.memory.consts
                    and not (value.type & FUNCTION)):
                del child.memory.addrs[name]

        child_x_token = child.memory.query("x")
        child_x_token.value = child_x
        child_y_token = child.memory.query("y")
        child_y_token.value = child_y
        child.memory.id =  uuid.uuid4()
        child.memory.alloc_const("x", child_x_token)
        child.memory.alloc_const("y", child_y_token)
        self.game.RunningCreatures.append(child)
        return NORMAL, None



GenericBuiltinFunctions = Builtins()