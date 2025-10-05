from enum import Enum

class Keywords(Enum):
    PRINT           = 'print'
    LET             = 'let'
    IF              = 'if'
    ELSE            = 'else'

class TokenType(Enum):
    REAL            = 0
    STRING          = 1
    BOOLEAN         = 2
    IDENTIFIER      = 3
    PARENTHESIS     = 4
    BRACE           = 5
    ARITHMETIC_OP   = 6
    RELATIONAL_OP   = 7
    EQUALITY_OP     = 8
    LOGICAL_OP      = 9
    ASSIGNMENT      = 10
    NOT_OP          = 11
    SEMICOLON       = 12
    COLON           = 13
    EOF             = 14

class Token:
    def __init__(self, _type: TokenType, index: int, length: int, source: str, line: int = 0):
        self.type = _type
        self.index = index
        self.length = length
        self.line = line
        self.source = source

    def __repr__(self) -> str:
        return f"[{self.type} : {self.source[self.index: self.index + self.length]} : {self.line}]"
    
    @property
    def lexeme(self) -> str:
        return self.source[self.index: self.index + self.length]