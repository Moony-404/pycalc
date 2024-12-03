# Tokens for the scanner
class Token:
    def __init__(self, repr: str):
        self.repr: str = repr
        
    def __repr__(self) -> str:
        return self.repr

    def __str__(self) -> str:
        return self.repr

class NumberToken(Token):  
    def __init__(self, value: float):
        super().__init__(str(value))
        self.value: float = value

class String(Token):
    def __init__(self, s: str):
        super().__init__(f'"{s}"')
        self.value: str = s

class Boolean(Token):
    def __init__(self, value: bool):
        super().__init__(str(value))
        self.value: bool = value

class Identifier(Token):
    def __init__(self, s: str):
        super().__init__(str(s))
        self.word : str = s

class Parenthesis(Token):
    def __init__(self, symbol: str):
        super().__init__(symbol)
        self.symbol: str = symbol

class Brace(Token):
    def __init__(self, symbol: str):
        super().__init__(symbol)
        self.symbol: str = symbol

class MathOP(Token):
    def __init__(self, op: str):
        super().__init__(op)
        self.op: str = op

class RelationalOP(Token):
    def __init__(self, op: str):
        super().__init__(op)
        self.op: str = op

class EqualityOP(Token):
    def __init__(self, op: str):
        super().__init__(op)
        self.op: str = op

class LogicalOP(Token):
    def __init__(self, op: str):
        super().__init__(op)
        self.op: str = op

class AssignmentOP(Token):
    def __init__(self):
        super().__init__("=")

class NotOP(Token):
    def __init__(self):
        super().__init__('not')

class Semicolon(Token):
    def __init__(self):
        super().__init__(';')

class EOFToken(Token):
    def __init__(self):
        super().__init__('EOF')
