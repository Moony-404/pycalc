from __future__ import annotations
from typing import List, Optional
import sys

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