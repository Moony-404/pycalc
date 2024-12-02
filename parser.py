from __future__ import annotations
import sys
from typing import List, Optional
from scanner import *
# from interpreter import Interpreter

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
  
class Expr:
    def accept(self, i: Interpreter) -> float:
        return float('inf')

class AssignmentExpr(Expr):
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

    def accept(self, i: Interpreter) -> float:
        return i.execute_binary_expr(self)    

class UnaryExpr(Expr):
    def __init__(self, expr: Expr):
        self.expr: Expr = expr

    def accept(self, i: Interpreter) -> float:
        return i.execute_unary_expr(self)

class LiteralExpr(Expr):
    def __init__(self, value: float):
        self.value: float = value

    def accept(self, i: Interpreter) -> float:
        return i.execute_literal_expr(self)

class IdentifierExpr(Expr):
    def __init__(self, word: str):
        self.word = word

    def accept(self, i: Interpreter) -> float:
        try:
            value = i.environment[self.word]
            return value
        except KeyError:
            print(f"Undefined variable '{self.word}'")
            sys.exit()

# Finally a class for parser
class Parser:
    def __init__(self):
        self.script: List[Stmt] = []
        self.index: int = 0
        self.tokens: List[Token] = []

    @property
    def current_token(self) -> Token:
        return self.tokens[self.index]

    @property
    def end_of_tokens(self) -> bool:
        return (True if self.index >= len(self.tokens) else False)

    def move_pointer(self) -> None:
        self.index += 1

    def parse(self, tokens: List[Token]):
        # Initialize the state of the parser
        self.tokens = tokens
        self.index = 0
        self.script = []

        if not self.end_of_tokens:
            self.script.append(self.parse_decl())

    def parse_decl(self) -> Stmt:

        if isinstance(self.current_token, IdentifierToken):
            if self.current_token.word == 'print':
                print_stmt : Stmt = self.parse_print_stmt()
                return print_stmt
            
            elif self.current_token.word == 'let':
                let_stmt : Stmt = self.parse_let_stmt()
                return let_stmt
        
        expr : Expr = self.parse_assignment()
        expr_stmt : ExprStmt = ExprStmt(expr)
        return expr_stmt

    def parse_print_stmt(self) -> PrintStmt:
        self.move_pointer()
        e : Expr = self.parse_expr()
        return PrintStmt(e)
    
    def parse_let_stmt(self) -> LetDecl:
        self.move_pointer()
        if isinstance(self.current_token, IdentifierToken):
            name = self.current_token.word
        else:
            print("Syntax Error: Expected a word after 'let'")
            sys.exit()
        
        self.move_pointer()
        if (not self.end_of_tokens) and isinstance(self.current_token, EqualityToken):
            self.move_pointer()
            e : Expr = self.parse_expr()
            return LetDecl(name, e)
        
        return LetDecl(name, None)

    def parse_assignment(self) -> Expr:
        lvalue: Expr = self.parse_expr()

        if (not self.end_of_tokens) and isinstance(self.current_token, EqualityToken) and isinstance(lvalue, IdentifierExpr):
            self.move_pointer()
            rvalue: Expr = self.parse_expr()
            return AssignmentExpr(lvalue.word, rvalue)
        
        return lvalue

    def parse_expr(self) -> Expr:
        left: Expr = self.parse_factor()

        if (not self.end_of_tokens) and isinstance(self.current_token, OperatorToken) and self.current_token.op in '+-':
            operator: str = self.current_token.op
            self.move_pointer()
            right: Expr = self.parse_expr()

            return BinaryExpr(left, operator, right)

        return left
        
    def parse_factor(self) -> Expr:
        left: Expr = self.parse_term()
        
        if (not self.end_of_tokens) and isinstance(self.current_token, OperatorToken) and self.current_token.op in '*/':
            operator: str = self.current_token.op
            self.move_pointer()
            right: Expr = self.parse_factor()

            return BinaryExpr(left, operator, right)

        return left

    def parse_term(self) -> Expr:

        # If we reached the end of list of tokens
        if (self.end_of_tokens):
            return LiteralExpr(0)

        if isinstance(self.current_token, NumericToken):
            literal: LiteralExpr = LiteralExpr(self.current_token.value)
            self.move_pointer()
            return literal
        
        elif isinstance(self.current_token, IdentifierToken):
            identifier: IdentifierExpr = IdentifierExpr(self.current_token.word)
            self.move_pointer()
            return identifier

        elif isinstance(self.current_token, OperatorToken) and self.current_token.op == '-':
            self.move_pointer()
            term: Expr = self.parse_term()
            return UnaryExpr(term)

        elif isinstance(self.current_token, ParenToken) and self.current_token.paren == '(':
            self.move_pointer()
            expr: Expr = self.parse_expr()

            if (not isinstance(self.current_token, ParenToken)) or (self.current_token.paren != ')'):
                print("Expected a ')'")
                sys.exit()
        
            self.move_pointer()
            return expr
        
        else:
            print("Invalid Syntax in parse_terms")
            sys.exit()

