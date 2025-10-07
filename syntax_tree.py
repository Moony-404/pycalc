from __future__ import annotations
from typing import List, Optional
from _token import Token
from abc import ABC
from enum import Enum


class NodeType(Enum):
    IDENTIFIER_NODE     = 0
    BOOL_NODE           = 1
    REAL_NODE           = 2
    
    INVERSION           = 3
    NEGATION            = 4
    FACTOR              = 5
    MODULO              = 6
    TERM                = 7
    COMPARISON          = 8
    EQUALITY            = 9
    LOGICAL             = 10
    ASSIGNMENT          = 11
    
    EXPR_STMT           = 12
    PRINT_STMT          = 13
    LET_STMT            = 14
    IF_STMT             = 15
    WHILE_STMT          = 16
    BLOCK_STMT          = 17

    STRING_NODE         = 18


class Node:
    def __init__(self, _type: NodeType, token: Token):
        self.type: NodeType = _type
        self.token: Token = token

    def __repr__(self) -> str:
        return f"[{self.type}: {self.token.lexeme}]"
    
class UnaryNode:
    def __init__(self, _type: NodeType, op: BinaryNode | UnaryNode | Node):
        self.type: NodeType = _type
        self.operand = op

class BinaryNode:
    def __init__(self, _type: NodeType, operator: Token, left: BinaryNode | UnaryNode | Node, right: BinaryNode | UnaryNode | Node):
        self.type: NodeType = _type
        self.operator: Token = operator
        self.operand = (left, right)

    def __repr__(self) -> str:
        return f"[{self.operand[0]} {self.operator} {self.operand[1]}]"
    
class Statement(ABC):
    def __init__(self, _type : NodeType):
        self.type = _type

class ExpressionStatement(Statement):
    def __init__(self, primary: BinaryNode | UnaryNode | Node ):
        self.type = NodeType.EXPR_STMT
        self.primary = primary

class BlockStatement(Statement):
    def __init__(self, array: List[Statement]):
        self.type = NodeType.BLOCK_STMT
        self.array = array

class LetStatement(Statement):
    def __init__(self, primary: Node, secondary: BinaryNode | UnaryNode | Node | None):
        self.type = NodeType.LET_STMT
        self.primary = primary
        self.secondary = secondary

class PrintStatement(Statement):
    def __init__(self, expressions: List[BinaryNode | UnaryNode | Node] ):
        self.type = NodeType.PRINT_STMT
        self.expressions = expressions

class IfStatement(Statement):
    def __init__(self, primary: Statement | None, expression: BinaryNode | UnaryNode | Node, secondary: Optional[Statement]):
        self.type = NodeType.IF_STMT
        self.primary = primary
        self.expression = expression
        self.secondary = secondary

class WhileStatement(Statement):
    def __init__(self, primary: Statement | None, expression: BinaryNode | UnaryNode | Node):
        self.type = NodeType.WHILE_STMT
        self.primary = primary
        self.expression = expression