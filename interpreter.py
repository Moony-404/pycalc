from __future__ import annotations
from parser import *
from scanner import *
from typing import List

class Interpreter:
    def __init__(self):
        self.scanner: Scanner= Scanner()
        self.parser: Parser = Parser()
        # A dictionary to contain all the variables and their bindings
        self.environment: dict = {}

    def run(self) -> None:
        while (True):
            user_input: str = input("> ")
            if user_input == 'exit' or user_input == 'quit':
                break
            self.scanner.scan(user_input)
            # print(self.scanner.tokens)
            self.parser.parse(self.scanner.tokens)
            self.execute(self.parser.script)

    def execute(self, script: List[Stmt]) -> None:
        for stmt in script:
            if isinstance(stmt, ExprStmt):
                value = stmt.accept(self)
                print(value)
            else:
                stmt.accept(self)

    def execute_logical_expr(self, expr: LogicalExpr) -> float:
        l: float = expr.left.accept(self)
        r: float = expr.right.accept(self)

        if expr.operator == 'and':
            return float(l and r)
        
        return float(l or r)
    
    def execute_equality_expr(self, expr: EqualityExpr) -> float:
        l: float = expr.left.accept(self)
        r: float = expr.right.accept(self)

        if expr.operator == '==':
            return float(l == r)
        
        return float(l != r)
    
    def execute_relational_expr(self, expr: RelationalExpr) -> float:
        l: float = expr.left.accept(self)
        r: float = expr.right.accept(self)

        if expr.operator == '<':
            return float(l < r)
        elif expr.operator == '<=':
            return float(l <= r)
        elif expr.operator == '>':
            return float(l > r)
        else:
            return float(l >= r)
        
    def execute_add_expr(self, expr: AddExpr) -> float:
        l: float = expr.left.accept(self)
        r: float = expr.right.accept(self)

        if expr.operator == '+':
            return l + r
        else:
            return l - r
        
    def execute_modulus_expr(self, expr: ModulusExpr) -> float:
        l: float = expr.left.accept(self)
        r: float = expr.right.accept(self)

        return int(l) % int(r)
    
    def execute_mul_expr(self, expr: MulExpr) -> float:
        l: float = expr.left.accept(self)
        r: float = expr.right.accept(self)

        if expr.operator == '*':
            return l * r
        else:
            return l / r
        
    def execute_negate_expr(self, expr: NegateExpr) -> float:
        value: float = -1 * expr.expr.accept(self)
        return value
    
    def execute_not_expr(self, expr: NotExpr) -> float:
        value: float = not expr.expr.accept(self)
        return float(value)

    def execute_number_node(self, n: NumberNode) -> float:
        return n.value
    
    def execute_bool_node(self, b: BooleanNode) -> float:
        return float(b.value)