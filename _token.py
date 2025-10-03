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
    def __init__(self, type: TokenType, lexeme: int, length: int, source: str, line: int = 0):
        self.type = type
        self.lexeme = lexeme
        self.length = length
        self.line = line
        self.source = source

    def __repr__(self) -> str:
        return f"[{self.type} : {self.source[self.lexeme: self.lexeme + self.length]} : {self.line}]"

# Tokens for the scanner
# class Token:
#     def __init__(self, repr: str):
#         self.repr: str = repr
        
#     def __repr__(self) -> str:
#         return self.repr

#     def __str__(self) -> str:
#         return self.repr

# class NumberToken(Token):  
#     def __init__(self, value: float):
#         super().__init__(str(value))
#         self.value: float = value

# class String(Token):
#     def __init__(self, s: str):
#         super().__init__(f'"{s}"')
#         self.value: str = s

# class Boolean(Token):
#     def __init__(self, value: bool):
#         super().__init__(str(value))
#         self.value: bool = value

# class Identifier(Token):
#     def __init__(self, s: str):
#         super().__init__(str(s))
#         self.word : str = s

# class Parenthesis(Token):
#     def __init__(self, symbol: str):
#         super().__init__(symbol)
#         self.symbol: str = symbol

# class Brace(Token):
#     def __init__(self, symbol: str):
#         super().__init__(symbol)
#         self.symbol: str = symbol

# class MathOP(Token):
#     def __init__(self, op: str):
#         super().__init__(op)
#         self.op: str = op

# class RelationalOP(Token):
#     def __init__(self, op: str):
#         super().__init__(op)
#         self.op: str = op

# class EqualityOP(Token):
#     def __init__(self, op: str):
#         super().__init__(op)
#         self.op: str = op

# class LogicalOP(Token):
#     def __init__(self, op: str):
#         super().__init__(op)
#         self.op: str = op

# class AssignmentOP(Token):
#     def __init__(self):
#         super().__init__("=")

# class NotOP(Token):
#     def __init__(self):
#         super().__init__('not')

# class Semicolon(Token):
#     def __init__(self):
#         super().__init__(';')

# class EOFToken(Token):
#     def __init__(self):
#         super().__init__('EOF')
