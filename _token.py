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
    INEQUALITY_OP   = 9
    LOGICAL_OP      = 10
    ASSIGNMENT      = 11
    NOT_OP          = 12
    SEMICOLON       = 13
    COLON           = 14

    PRINT           = 15
    LET             = 16
    IF              = 17
    ELSE            = 18
    WHILE           = 19
    THEN            = 20
    DO              = 21

    EOF             = 22


Reserved = {
    'print'         : TokenType.PRINT,
    'let'           : TokenType.LET,
    'if'            : TokenType.IF,
    'else'          : TokenType.ELSE,
    'while'         : TokenType.WHILE,
    'do'            : TokenType.DO,
    'then'          : TokenType.THEN,

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