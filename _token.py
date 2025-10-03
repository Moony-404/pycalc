from enum import Enum

class TokenType(Enum):
    REAL            = 0
    STRING          = 1
    BOOLEAN         = 2
    IDENTIFIER      = 3
    PARENTHESIS     = 4
    BRACE           = 5
    ARITHMETIC_OP   = 6
    RELATIONAL_OP   = 7
    LOGICAL_OP      = 8
    EQUALITY_OP     = 9
    ASSIGNMENT      = 10
    NOT_OP          = 11
    SEMICOLON       = 12
    EOF             = 13

class Token:
    def __init__(self, type: TokenType, index: int, length: int, source: str, line: int = 0):
        self.type = type
        self.index = index
        self.length = length
        self.line = line
        self.source = source

    def __repr__(self) -> str:
        return f"[{self.type} : {self.source[self.index: self.index + self.length]} : {self.line}]"
    
    @property
    def lexeme(self) -> str:
        return self.source[self.index: self.index + self.length]