class InterpreterException(Exception):
    line = 0
    def __init__(self):
        self.error = "Interpreter unknow exception [__line__]"

    def AddLine(self, line):
        if not isinstance(line, int):
            raise Exception(f"invalid line: [{line}]")

        self.error = self.error.replace("__line__", str(line))

class MemoryException(InterpreterException):
    def __init__(self, err = ""):
        super().__init__()
        self.error = "Memory exception at line [__line__]" + " " + err


class MissingVariable(InterpreterException):
    def __init__(self,var):
        super().__init__()
        self.error = f"Variable not declared [{var}] at line [__line__]"


class StructureException(InterpreterException):
    def __init__(self, error):
        super().__init__()
        self.error = error + " [__line__]"

class ExpresionException(InterpreterException):
    def __init__(self, error):
        super().__init__()
        self.error = error + " [__line__]"

class ZeroDivisionException(InterpreterException):
    def __init__(self, error):
        super().__init__()
        self.error = error + " [__line__]"

class SintaxisException(InterpreterException):
    def __init__(self, error):
        super().__init__()
        self.error = error + " [__line__]"

class CallFuncException(InterpreterException):
    def __init__(self, error):
        super().__init__()
        self.error = error + " [__line__]"
