from modules.game.typesutil import *
from modules.game.static import *
from modules.game.initializer import *


class GameTerrainBuilder:
    terrain = None
    char = None
    resource_max = None
    regen = None

    def Initialize(self,data):
        return Initialize(self, data)
    
    def ToTerrain(self) -> GameTerrain:
        return GameTerrain(self.char, self.terrain, self.resource_max, self.regen)

class GameTerrain(GameJson):

    Regen = 0
    def __init__(self, char, name, cnt, reg):
        self.Char = char
        self.Name = name
        self.Count = cnt
        self.Regen = reg
        self.Max = cnt

    def __dict__(self):
        di:dict = super().__dict__()
        di["Regen"] = self.Regen
        return di

    def copy(self):
        return GameTerrain(self.Char, self.Name, self.Count, self.Regen)