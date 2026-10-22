
from modules.game.types.initializer import *
from modules.game.static import *
from modules.game.typesutil import *

class GameObjectBuilder:
    object = ""
    char = ""
    resource_max = 0

    def Initialize(self, buff: bytes):
        return Initialize(self, buff)

    def ToObject(self):
        return GameObject(self.object, self.char, self.resource_max)


class GameObject(GameJson):
    def __init__(self, name, chr, cnt):
        self.Name = name
        self.Char = chr
        self.Count = cnt
        self.Max = cnt

    def __dict__(self):
        return super().__dict__()

    def copy(self):
        cp = GameObject(self.Name, self.Char, self.Max)
        cp.Count = self.Count
        return cp