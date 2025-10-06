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
    EQUALITY_OP     = 8
    LOGICAL_OP      = 9
    ASSIGNMENT      = 10
    NOT_OP          = 11
    SEMICOLON       = 12
    COLON           = 13

    PRINT           = 14
    LET             = 15
    IF              = 16
    ELSE            = 17
    WHILE           = 18

    EOF             = 19


Reserved = {
    'print'         : TokenType.PRINT,
    'let'           : TokenType.LET,
    'if'            : TokenType.IF,
    'else'          : TokenType.ELSE,
    'while'         : TokenType.WHILE,

    # OPERATORS

    'and'           : TokenType.LOGICAL_OP,
    'or'            : TokenType.LOGICAL_OP,
    'not'           : TokenType.LOGICAL_OP,

    # VALUES

    'True'          : TokenType.BOOLEAN,
    'False'         : TokenType.BOOLEAN
}

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