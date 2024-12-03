from __future__ import annotations
from typing import List, Optional
import sys

# Nodes of the AST, to be created by Recursive Descent Parsing

class Stmt:
    def accept(self, i: Interpreter):
        pass

class LetDecl(Stmt):
    def __init__(self, name : str, expr: Optional[Expr]):
        self.name: str = name
        self.expr: Optional[Expr] = expr

    def accept(self, i: Interpreter) -> Optional[float]:
        if self.expr is None:
            return None
        value: float = self.expr.accept(i)
        i.environment[self.name] = value
        return value
    
class ExprStmt(Stmt):
    def __init__(self, expr: Expr):
        self.expr: Expr = expr

    def accept(self, i: Interpreter) -> float:
        return self.expr.accept(i)

class PrintStmt(Stmt):
    def __init__(self, expr: Expr):
        self.expr: Expr = expr

    def accept(self, i: Interpreter) -> None:
        print(self.expr.accept(i))

# Classes for expressions  
class Expr:
    def accept(self, i: Interpreter) -> float:
        return float('inf')

class Assignment(Expr):
    def __init__(self, word: str, expr: Expr):
        self.word = word
        self.expr = expr

    def accept(self, i: Interpreter) -> float:
        if self.word in i.environment:
            value : float = self.expr.accept(i)
            i.environment[self.word] = value
            return value
        
        print(f"Name Error: Variable {self.word} does not exist")
        sys.exit()
        
class BinaryExpr(Expr):
    def __init__(self, left: Expr, operator: str, right: Expr):
        self.left: Expr = left
        self.operator: str = operator
        self.right: Expr = right

    def accept(self, i: Interpreter):
        pass

class LogicalExpr(BinaryExpr):
    def __init__(self, left: Expr, operator: str, right: Expr):
        super().__init__(left, operator, right)

    def accept(self, i: Interpreter) -> float:
        return i.execute_logical_expr(self)
    
class EqualityExpr(BinaryExpr):
    def __init__(self, left: Expr, operator: str, right: Expr):
        super().__init__(left, operator, right)

    def accept(self, i: Interpreter) -> float:
        return i.execute_equality_expr(self)
    
class RelationalExpr(BinaryExpr):
    def __init__(self, left: Expr, operator: str, right: Expr):
        super().__init__(left, operator, right)

    def accept(self, i: Interpreter) -> float:
        return i.execute_relational_expr(self)
    
class AddExpr(BinaryExpr):
    def __init__(self, left: Expr, operator: str, right: Expr):
        super().__init__(left, operator, right)

    def accept(self, i: Interpreter) -> float:
        return i.execute_add_expr(self)
    
class ModulusExpr(BinaryExpr):
    def __init__(self, left: Expr,  right: Expr):
        super().__init__(left, '%', right)

    def accept(self, i: Interpreter) -> float:
        return i.execute_modulus_expr(self)

class MulExpr(BinaryExpr):
    def __init__(self, left: Expr, operator: str, right: Expr):
        super().__init__(left, operator, right)

    def accept(self, i: Interpreter) -> float:
        return i.execute_mul_expr(self)

class UnaryExpr(Expr):
    def __init__(self, expr: Expr):
        self.expr: Expr = expr

class NegateExpr(UnaryExpr):
    def __init__(self, expr: Expr):
        super().__init__(expr)

    def accept(self, i: Interpreter) -> float:
        return i.execute_negate_expr(self)
    
class NotExpr(UnaryExpr):
    def __init__(self, expr: Expr):
        super().__init__(expr)

    def accept(self, i: Interpreter) -> float:
        return i.execute_not_expr(self)

class Primary(Expr):
    pass
class NumberNode(Primary):
    def __init__(self, value: float):
        self.value: float = value

    def accept(self, i: Interpreter) -> float:
        return i.execute_number_node(self)
    
class BooleanNode(Primary):
    def __init__(self, value: bool):
        self.value : bool = value

    def accept(self, i: Interpreter) -> float:
        return i.execute_bool_node(self)

class IdentifierNode(Expr):
    def __init__(self, word: str):
        self.word = word

    def accept(self, i: Interpreter) -> float:
        try:
            value = i.environment[self.word]
            return value
        except KeyError:
            print(f"Undefined variable '{self.word}'")
            sys.exit()