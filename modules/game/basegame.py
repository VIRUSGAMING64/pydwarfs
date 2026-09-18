from modules.game.terrains import *
from modules.game.objects import *
from modules.game.map import *

from modules.game.map import GameMap
import logging
import os
logging.basicConfig(level=logging.DEBUG)

DEFAULT_O_PATH = "gamedata/objets"
DEFAULT_T_PATH = "gamedata/terrains"
DEFAULT_M_PATH = "gamedata/maps"

class Game:
    m_path = DEFAULT_M_PATH
    t_path = DEFAULT_T_PATH
    o_path = DEFAULT_O_PATH
    Terrains:list[GameTerrain] = []
    Objects:list[GameObject] = []
    Maps:list[GameMap] = []
    def __init__(self, m_path = DEFAULT_M_PATH, t_path = DEFAULT_T_PATH, o_path = DEFAULT_O_PATH):
        os.makedirs(m_path, exist_ok=True)
        os.makedirs(t_path, exist_ok=True)
        os.makedirs(o_path, exist_ok=True)
        self.o_path = o_path
        self.t_path = t_path
        self.m_path = m_path

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
        }