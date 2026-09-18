from modules.game.terrains import *
from modules.game.objects import *

from modules.game.map import Map
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
    Maps:list[Map] = []
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
                base = GameBaseTerrain()  
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
            logging.debug(f"paths: [{pth}]")
            with open(pth, "rb") as file:
                buff = file.read()
                base = GameBaseObject()
                if base.Initialize(buff):
                    self.Objects.append(base.ToObject())