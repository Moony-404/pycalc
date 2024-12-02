from __future__ import annotations
from parser import *
from scanner import *
from typing import List, Optional
import sys

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
            self.parser.parse(self.scanner.tokens)
            self.execute(self.parser.script)

    def execute(self, script: List[Stmt]) -> None:
        for stmt in script:
            if isinstance(stmt, ExprStmt):
                value = stmt.accept(self)
                print(value)
            else:
                stmt.accept(self)

    def execute_binary_expr(self, expr: BinaryExpr) -> float:
        l : float = expr.left.accept(self)
        r : float = expr.right.accept(self)

        if expr.operator == '+':
            return l + r
        elif expr.operator == '-':
            return l - r
        elif expr.operator == '*':
            return l * r
        elif expr.operator == '/':
            if (r == 0):
                print("Math Error: Divide by zero.")
                sys.exit() 
            return l / r
        else:
            print(f"Syntax Error: Unknown operator '{expr.operator}'")
            sys.exit()

    def execute_literal_expr(self, literal: LiteralExpr) -> float:
        return literal.value
    
    def execute_unary_expr(self, unary: UnaryExpr) -> float:
        return -1 * unary.expr.accept(self)