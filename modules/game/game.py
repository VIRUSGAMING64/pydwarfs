from modules.game.terrains import *
from modules.game.objects import *
from modules.game.map import *
from modules.interpreter import *
from modules.game.map import GameMap
from modules.game.maths import *
import logging
import os

logging.basicConfig(level=logging.DEBUG)

DEFAULT_O_PATH = "gamedata/objets"
DEFAULT_T_PATH = "gamedata/terrains"
DEFAULT_M_PATH = "gamedata/maps"
DEFAULT_C_PATH = "gamedata/entity"
GREATER = 2**64 - 1

class Game:
    m_path = DEFAULT_M_PATH
    t_path = DEFAULT_T_PATH
    o_path = DEFAULT_O_PATH
    Terrains:list[GameTerrain] = None
    Objects:list[GameObject] = None
    Maps:list[GameMap] = None
    Creatures :list[Interpreter] = None
    
    def __init__(self, m_path = DEFAULT_M_PATH, t_path = DEFAULT_T_PATH, o_path = DEFAULT_O_PATH, c_path = DEFAULT_C_PATH):
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
        self.Creatures = []

    def LoadTerrains(self):
        try:
            data = os.listdir(self.t_path)
        except Exception as e:
            logging.error(f"unable to load terrains [{e}]")
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
            logging.error(f"unable to load objects [{e}]")
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
            logging.error(f"unable to load maps [{e}]")
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
                        #! reportar error del mapa
                        continue
                    self.Maps.append(mapa)

    def LoadCreatures(self):
        try:
            data = os.listdir(self.c_path)
        except Exception as e:
            logging.error(f"unable to load creatures [{e}]")
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

    def GetPerseption(self, c: Interpreter):
        minAdis = GREATER #* no creo q vayan hacer un mapa tan grande
        allx = 0
        ally = 0

        minEdis = GREATER #* no creo q vayan hacer un mapa tan grande
        Ex = 0 #* Este es los dx del enemy
        Ey = 0       

        currx = c.query("x")
        curry = c.query("y")
        allys = 0
        enemis = 0

        for cre in self.Creatures:
            x=cre.query("x")
            y=cre.query("y")
            dis = p2dist(x,y,currx, curry)
            if dis > c.vision:
                continue
            if cre.faction == c.faction:
                allys += 1
                if dis < minAdis:
                    allx = parsedirection(x,currx)
                    ally = parsedirection(y,curry)
            else:
                enemis += 1 
                if dis < minEdis:
                    Ex = parsedirection(x,currx)
                    Ey = parsedirection(y,curry)

        if minAdis == GREATER:
            minAdis = -1
        if minEdis == GREATER:
            minEdis = -1

        c.alloc("enemy_dx", Ex)
        c.alloc("enemy_dy", Ey)
        c.alloc("ally_dx", allx)
        c.alloc("ally_dy", ally)
        c.alloc("enemy_dist", minEdis)
        c.alloc("ally_dist", minAdis)
        c.alloc("allies_near", allys)

    def Step(self):
        for creature in self.Creatures:
            self.GetPerseption(creature)
            creature.Step()

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
            "creatures": [i.__dict__() for i in self.Creatures]
        }