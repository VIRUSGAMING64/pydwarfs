from modules.game.types.terrains import *
from modules.game.types.objects import *
from modules.game.types.map import *
from modules.interpreter import *
from modules.game.types.map import GameMap
from modules.game.utils import *
from modules.game.maths import *
import os

DEFAULT_O_PATH = "gamedata/objets"
DEFAULT_T_PATH = "gamedata/terrains"
DEFAULT_M_PATH = "gamedata/maps"
DEFAULT_C_PATH = "gamedata/entity"
GREATER = 2**64 - 1


class Roar:
    def __init__(self):
        self.Roars = []
    
    def PostRoar(self,roar):
        self.Roars.append(roar)

    def PopLastRoar(self):
            return self.Roars.pop()

    def PopFirstRoar(self):
            return self.Roars.pop(0)
        
class Game(Roar):
    m_path = DEFAULT_M_PATH
    t_path = DEFAULT_T_PATH
    o_path = DEFAULT_O_PATH
    Terrains:list[GameTerrain] = None
    Objects:list[GameObject] = None
    Maps:list[GameMap] = None
    Creatures :list[Interpreter] = None
    RunningCreatures: list[Interpreter] = None
    
    def __init__(self, m_path = DEFAULT_M_PATH, t_path = DEFAULT_T_PATH, o_path = DEFAULT_O_PATH, c_path = DEFAULT_C_PATH):
        super().__init__()
        os.makedirs(m_path, exist_ok=True)
        os.makedirs(t_path, exist_ok=True)
        os.makedirs(o_path, exist_ok=True)
        os.makedirs(c_path, exist_ok=True)
        self.o_path = o_path
        self.t_path = t_path
        self.m_path = m_path
        self.c_path = c_path
        self.Objects = []
        self.Terrains = []
        self.Maps = []
        self.RunningCreatures = []
        self.Creatures = []

    def LoadTerrains(self):
        try:
            data = os.listdir(self.t_path)
        except Exception as e:
            print(e)
            return
        for pth in data:
            if not pth.endswith(".te"):
                continue
            pth = os.path.join(self.t_path, pth)
            lines = [] 
            with open(pth, "rb") as file:
                buff = file.read()
                base = GameTerrainBuilder()  
                if base.Initialize(buff):
                    self.Terrains.append(base.ToTerrain())

    def LoadObjects(self):
        try:
            data = os.listdir(self.o_path)
        except Exception as e:
            print(f"unable to load objects [{e}]")
            return
        for pth in data:
            if not pth.endswith(".ob"):
                continue
            pth = os.path.join(self.o_path, pth)
            with open(pth, "rb") as file:
                buff = file.read()
                base = GameObjectBuilder()
                if base.Initialize(buff):
                    self.Objects.append(base.ToObject())
                

    def LoadMaps(self):
        try:
            data = os.listdir(self.m_path)
        except Exception as e:
            print(f"unable to load maps [{e}]")
            return
        for pth in data:
            if not pth.endswith(".map"):
                continue
            pth = os.path.join(self.m_path, pth)
            with open(pth, "rb") as file:
                buff = file.read()
                base = GameBaseMap()
                if base.Initialize(buff):
                    mapa = base.ToMap(self.Objects, self.Terrains)
                    if not isinstance(mapa, GameMap):
                        print(mapa)
                        raise Exception("error aqui")
                        #! reportar error del mapa
                        continue
                    self.Maps.append(mapa)

    def LoadCreatures(self):
        try:
            data = os.listdir(self.c_path)
        except Exception as e:
            print(f"unable to load creatures [{e}]")
            return
        for pth in data:
            if not pth.endswith(".ins"):
                continue
            pth = os.path.join(self.c_path, pth)
            with open(pth, "rb") as file:
                buff = file.read()
                try:
                    base = Interpreter(buff.decode())
                    self.Creatures.append(base)
                except Exception as e:
                    print(f"Error loading creature [{e}] in {pth}")
                    raise e

    def GetPerseption(self, c: Interpreter):
        minAdis = GREATER #* no creo q vayan hacer un mapa tan grande
        allx = 0
        ally = 0

        minEdis = GREATER #* no creo q vayan hacer un mapa tan grande
        Ex = 0 #* Este es los dx del enemy
        Ey = 0       

        currx = c.query("x").value
        curry = c.query("y").value
        allys = 0
        enemis = 0

        for cre in self.RunningCreatures:
            if c.memory.id == cre.memory.id:
                continue
            x=cre.query("x").value
            y=cre.query("y").value
            dis = p2dist(x,y,currx, curry)
            if dis > c.Vision().value:
                continue
            if cre.Faction().value == c.Faction().value:
                allys += 1
                if dis == 0:
                    continue
                if dis < minAdis:
                    minAdis = dis
                    allx = parsedirection(x,currx)
                    ally = parsedirection(y,curry)
            else:
                enemis += 1 
                if dis < minEdis:
                    minEdis = dis
                    Ex = parsedirection(x,currx)
                    Ey = parsedirection(y,curry)

        if minAdis == GREATER:
            minAdis = -1
        if minEdis == GREATER:
            minEdis = -1

        c.memory.alloc_const("enemy_dx", Token(Ex, NUMBER))
        c.memory.alloc_const("enemy_dy", Token(Ey, NUMBER))
        c.memory.alloc_const("ally_dx", Token(allx, NUMBER))
        c.memory.alloc_const("ally_dy", Token(ally, NUMBER))
        c.memory.alloc_const("enemy_dist", Token(minEdis, NUMBER))
        c.memory.alloc_const("ally_dist", Token(minAdis, NUMBER))
        c.memory.alloc_const("allies_near", Token(allys, NUMBER))
        c.memory.alloc_const("enemies_near", Token(enemis, NUMBER))

    def GetEntityAt(self,x,y):
        for it in self.RunningCreatures:
            t_x = it.memory.query("x").value
            t_y = it.memory.query("y").value
            if t_x == x and t_y == y:
                return it
        
    def IsInsideMap(self, x, y):
        if not self.Maps:
            return False
        grid = self.Maps[0].Grid #TODO: support multiple maps
        return 0 <= y < len(grid) and 0 <= x < len(grid[y])

    def GetObjectAt(self, x,y):
        if not self.IsInsideMap(x, y):
            return None
        element = self.Maps[0].Grid[y][x] #TODO: support multiple maps
        if isinstance(element, GameObject):
            return element
        return None

    def Clean(self):
        NCreatures = []
        for creature in self.RunningCreatures:
            if creature.Health().value > 0 and creature.Lifespan().value > 0:
                NCreatures.append(creature)
            else:
                print("debug: MURIO UNA CRIATURA: ", creature.memory)
                del creature
            self.RunningCreatures = NCreatures

    def Step(self):
        p = False
        for idx in RandPermutation(0, len(self.RunningCreatures)-1, len(self.RunningCreatures), time.time_ns()):
            creature = self.RunningCreatures[idx]
            self.GetPerseption(creature)
            p|=creature.Step()
            creature.ReduceLifespan()
        self.Clean()
        return p

    def GetTerrainAt(self, x,y):
        if not self.IsInsideMap(x, y):
            return None
        element = self.Maps[0].Grid[y][x] #TODO: support multiple maps
        if isinstance(element, GameTerrain):
            return element
        return self.Terrains[0].copy()
    
    def __dict__(self):
        return {
            "paths": {
                "objects": self.o_path,
                "terrains": self.t_path,
                "maps": self.m_path
            },
            "objects": [ob.__dict__() for ob in self.Objects],
            "terrains": [te.__dict__() for te in self.Terrains],
            "maps": [ma.__dict__() for ma in self.Maps],
            "creatures": [i.__dict__() for i in self.Creatures],
            "runningCreatures": [i.__dict__() for i in self.RunningCreatures]
        }
