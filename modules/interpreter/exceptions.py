class InterpreterException(Exception):
    line = 0
    def __init__(self):
        self.error = "Interpreter unknow exception [__line__]"

    def AddLine(self, line):
        if not isinstance(line, int):
            raise Exception(f"invalid line: [{line}]")

        self.error = self.error.replace("__line__", str(line))

class MemoryException(InterpreterException):
    def __init__(self):
        super().__init__()
        self.error = "Memory exception at line [__line__]"