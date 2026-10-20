from modules.interpreter.tokens.token import Token
from modules.interpreter.statics import *
from modules.interpreter.exceptions import *

def cleanStr(s: str) -> str:
    while s.startswith(" "):
        s = s.removeprefix(" ")
    while s.endswith(" "):
        s = s.removesuffix(" ")
    return s


class Lexer:

    def __init__(self, code, output):
        code = code.replace("\t","  ")
        code = code.replace("\r","  ")
        code = code.split("\n")
        self.code = code
        self.output = output
        self.output["Errors"] = []

    def Tokenize(self, expr: str) -> list[Token]:
        pos = 0
        act_tok = ""
        tokens = []
        start_str = None
        in_str = False
        while pos <= len(expr):
            if ((pos < len(expr)) and ((not expr[pos] in operators)) or in_str):
                act_tok += expr[pos]

                if start_str == None and expr[pos] in ["\"", "\'"]:
                    in_str = not in_str
                    start_str = expr[pos]
                
                elif expr[pos] == start_str:
                    in_str = not in_str
                    start_str = None

            else:
                dis = -1        
                act_tok = cleanStr(act_tok)
                tokens.append(
                    Token(act_tok)
                  )

                if pos < len(expr):            
                    dis -= 1
                
                p = False
                if act_tok == "":
                    tokens.pop()
                    p = True

                if dis == -2:
                    tokens.append(Token(expr[pos]))
                    while pos + 1 != len(expr) and expr[pos] + expr[pos + 1] in operators:
                        tokens[len(tokens) - 1].value += expr[pos + 1]
                        pos += 1
            
                if p: 
                    pos += 1
                    continue
                
                t_token:Token = tokens[len(tokens) + dis]
                le = len(t_token.value)
                t_token.GetType(operators, keywords)

                act_tok = ""

            pos += 1
            
        line_tokens = []

        for i in range(len(tokens)):
            line:Token = tokens[i]
            if line.type == NIL:
                splited_tokens = self.getErrs(line.value)
                for t in splited_tokens:
                    if t == []:
                        continue
                    line_tokens.append(t[0])        
            else:
                line_tokens.append(line)      
        for t in line_tokens:
            if t.type == NIL:
                raise SintaxisException(f"Sintax error with token [{t.value}]")           

        return line_tokens
        
    def getErrs(self,  expr):
        expr = expr.split(' ')
        if len(expr) == 1:
            tk = Token(expr[0])
            tk.GetType(operators, keywords)
            return [[tk]]
        arr = []
        for x in expr:
            arr.append(self.Tokenize(x))

        return arr

    def str2Token(self,expr):
        expr = cleanStr(expr)
        res = self.Tokenize(expr)
        li = Token(expr)
        li.type = LINE
        li.subtokens = res
        return li

    def TokenizeSource(self)-> list[Token]:
        lines = []
        p = 0
        for line in self.code:
            p += 1
            li = self.ProcessRawLine(line, p)
            if li == None:
                continue
            lines.append(li)
        return lines

    def ProcessRawLine(self, line: str, p):
        line = line.strip()
        if line == "": 
            return None
        
        t_line = self.str2Token(line)
        t_line.line = p
        
        for j in range(len(t_line.subtokens)):
            if t_line.subtokens[j].value == "#":
                t_line.subtokens[j].type = COMMENT
                t_line.subtokens[j].subtokens = t_line.subtokens[j+1:]
                del t_line.subtokens[j+1:]
                break

            t_line.subtokens[j].line = p

        for j in t_line.subtokens:
            #TODO check if is hex
            if j.type == NIL:
                self.output["Errors"].append(f"invalid token at line: {p}")
        return t_line