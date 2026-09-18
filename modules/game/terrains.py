
""" file.te
terrain Grass
char .
resource_max 100
regen 2
"""

class GameBaseTerrain:
    terrain = None
    char = None
    resource_max = None
    regen = None

    def Initialize(self,data):
        data = data.decode()
        lines = data.split('\n')
        
        for line in lines:
            props = line.split(' ')
            if len(props) != 2:
                #* Invalid terrain file
                return False
            attr:str = props[0]
            val :str  = props[1]
            if val.isnumeric():
                val = int(val)
            if not hasattr(self, attr):
                return False
            setattr(self, attr, val)
        return True
    
    def ToTerrain(self) -> GameTerrain:
        return GameTerrain(self.char, self.terrain, self.resource_max, self.regen)

class GameTerrain:
    Char = ""
    Name = ""
    Count = 0
    Max = 0
    Regen = 0
    def __init__(self, char, name, cnt, reg):
        self.Char = char
        self.Name = name
        self.Count = cnt
        self.Regen = reg
        self.Max = cnt

    def __dict__(self):
        return {
            "Name": self.Name,
            "Char": self.Char,
            "Count": self.Count,
            "Max": self.Max,
            "Regen": self.Regen
        }