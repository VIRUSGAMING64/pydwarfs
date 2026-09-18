
from modules.game.initializer import *

class GameBaseMap:
    name = ""
    strings = []

    def Initialize(self, buff): 
        buff = buff.decode().split("\n")
        if len(buff) == 0:
            return False
        self.name = buff[0]
        self.strings = buff[1:]
        if len(self.strings) == 0:
            return False
        
        baselen = len(self.strings[0])
        for line in self.strings:
            if len(line) != baselen:
                return False
        return True

    def ToMap(self, obj, terr):
        ops = {}
        for i in terr:
            if ops.get(i.Char) != None:
                continue
            ops[i.Char] = i

        for i in obj:
            if ops.get(i.Char) != None:
                continue
            ops[i.Char] = i

        ma = []
        i = 0
        for line in self.strings:
            j = 0
            mps = []
            for elem in line:
                tp = ops.get(elem)
                if tp == None:
                    return (i,j)
                mps.append(tp.copy())
                j += 1
            i += 1
            ma.append(mps)

        return GameMap(self.name, ma)
        
                    
class GameMap: 
    Grid:list = []
    Name = ""
    def __init__(self, name, grid):
        self.Grid = grid
        self.Name = name

    def __dict__(self):
        grid = [] 
        for line in self.Grid:
            tmp = []
            for k in line:
                tmp.append(k.__dict__())
            grid.append(tmp)
        return {
            "Name": self.Name,
            "Grid": grid
        }