class GameJson:
    Type = 0
    Name = ""
    Char = ""
    Max = 0
    Count = 0
    def __dict__(self):
        return {
            "Name": self.Name,
            "Char": self.Char,
            "Count": self.Count,
            "Max": self.Max,
            "Type": self.Type
        }
