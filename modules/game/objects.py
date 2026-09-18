class GameBaseObject:
    object = ""
    char = ""
    resource_max = 0

    def Initialize(self, buff: bytes):
        buff = buff.decode()
        lines = buff.split("\n")
        for line in lines:
            line = line.split(' ')
            if len(line) != 2:
                return False
            attr = line[0]
            val = line[1]
            if not hasattr(self, attr):
                return False

            setattr(self, attr, val)

        return True

    def ToObject(self):
        return GameObject(self.object, self.char, self.resource_max)

class GameObject:
    Name = ""
    Char = ""
    Max = 0
    Count = 0
    def __init__(self, name, chr, cnt):
        self.Name = name
        self.Char = chr
        self.Count = cnt
        self.Max = cnt

    def __dict__(self):
        return {
            "Name": self.Name,
            "Char": self.Char,
            "Count": self.Count,
            "Max": self.Max
        }