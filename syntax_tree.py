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
    ...

class ExpressionStatement(Statement):
    def __init__(self, primary: BinaryNode | UnaryNode | Node | None):
        self.type = NodeType.EXPR_STMT
        self.primary = primary

class LetStatement(Statement):
    def __init__(self, primary: Node, secondary: BinaryNode | UnaryNode | Node | None):
        self.type = NodeType.LET_STMT
        self.primary = primary
        self.secondary = secondary

class PrintStatement(Statement):
    def __init__(self, primary: BinaryNode | UnaryNode | Node | None):
        self.type = NodeType.PRINT_STMT
        self.primary = primary

class IfStatement(Statement):
    def __init__(self, primary: Statement | None, expression: BinaryNode | UnaryNode | Node, secondary: Optional[Statement]):
        self.type = NodeType.IF_STMT
        self.primary = primary
        self.expression = expression
        self.secondary = secondary


# Base Classes
class Stmt:
    AST_ID = -1

class Expr:
    AST_ID = -1

class BinaryExpr(Expr):
    def __init__(self, left: Expr, operator: str, right: Expr):
        self.left: Expr = left
        self.operator: str = operator
        self.right: Expr = right

class UnaryExpr(Expr):
    def __init__(self, expr: Expr):
        self.expr: Expr = expr

class Primary(Expr):
    ...

class IfStmt(Stmt):
    AST_ID = 15

    def __init__(self, expr: Expr, p: Optional[Stmt], q: Optional[Stmt]):
        self.condition = expr
        self.true_stmt = p
        self.false_stmt = q
        
class LetStmt(Stmt):
    AST_ID = 14

    def __init__(self, name : str, expr: Optional[Expr]):
        self.name: str = name
        self.expr: Optional[Expr] = expr
    
class ExprStmt(Stmt):
    AST_ID = 13

    def __init__(self, expr: Expr):
        self.expr: Expr = expr

class PrintStmt(Stmt):
    AST_ID = 12

    def __init__(self, expr: Expr):
        self.expr: Expr = expr

class Assignment(Expr):
    AST_ID = 11

    def __init__(self, word: str, expr: Expr):
        self.word = word
        self.expr = expr
        
class LogicalExpr(BinaryExpr):
    AST_ID = 10

    def __init__(self, left: Expr, operator: str, right: Expr):
        super().__init__(left, operator, right)

class EqualityExpr(BinaryExpr):
    AST_ID = 9

    def __init__(self, left: Expr, operator: str, right: Expr):
        super().__init__(left, operator, right)
    
class RelationalExpr(BinaryExpr):
    AST_ID = 8

    def __init__(self, left: Expr, operator: str, right: Expr):
        super().__init__(left, operator, right)
    
class AddExpr(BinaryExpr):
    AST_ID = 7
    
    def __init__(self, left: Expr, operator: str, right: Expr):
        super().__init__(left, operator, right)
    
class ModulusExpr(BinaryExpr):
    AST_ID = 6
    def __init__(self, left: Expr,  right: Expr):
        super().__init__(left, '%', right)

class MulExpr(BinaryExpr):
    AST_ID = 5

    def __init__(self, left: Expr, operator: str, right: Expr):
        super().__init__(left, operator, right)


class NegateExpr(UnaryExpr):
    AST_ID = 4

    def __init__(self, expr: Expr):
        super().__init__(expr)
    
class NotExpr(UnaryExpr):
    AST_ID = 3
    
    def __init__(self, expr: Expr):
        super().__init__(expr)

class NumberNode(Primary):
    AST_ID = 2
    
    def __init__(self, value: float):
        self.value: float = value
    
class BooleanNode(Primary):
    AST_ID = 1

    def __init__(self, value: bool):
        self.value : bool = value

class IdentifierNode(Expr):
    AST_ID = 0

    def __init__(self, word: str):
        self.word = word