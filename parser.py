from __future__ import annotations
import sys
from typing import List
from scanner import *
from AST import *
# from interpreter import Interpreter

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
        return isinstance(self.current_token, EOFToken)

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
        if isinstance(self.current_token, Identifier):
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
        e : Expr = self.parse_assignment()
        return PrintStmt(e)
    
    def parse_let_stmt(self) -> LetDecl:
        self.move_pointer()
        if isinstance(self.current_token, Identifier):
            name = self.current_token.word
        else:
            print("Syntax Error: Expected a variable name after 'let'")
            sys.exit()
        
        self.move_pointer()
        if (not self.end_of_tokens) and isinstance(self.current_token, AssignmentOP):
            self.move_pointer()
            e : Expr = self.parse_assignment()
            return LetDecl(name, e)
        
        return LetDecl(name, None)

    def parse_assignment(self) -> Expr:
        lvalue: Expr = self.parse_logical_expr()

        if (not self.end_of_tokens) and isinstance(self.current_token, AssignmentOP) and isinstance(lvalue, IdentifierNode):
            self.move_pointer()
            rvalue: Expr = self.parse_logical_expr()
            return Assignment(lvalue.word, rvalue)
        
        return lvalue
    
    def parse_logical_expr(self) -> Expr:
        left: Expr = self.parse_equality_expr()

        if (not self.end_of_tokens) and isinstance(self.current_token, LogicalOP):
            operator: str = self.current_token.op
            self.move_pointer()
            right: Expr = self.parse_logical_expr()
            return LogicalExpr(left, operator, right)
        
        return left
    
    def parse_equality_expr(self) -> Expr:
        left: Expr = self.parse_relational_expr()

        if (not self.end_of_tokens) and isinstance(self.current_token, EqualityOP):
            operator: str = self.current_token.op
            self.move_pointer()
            right: Expr = self.parse_equality_expr()
            return EqualityExpr(left, operator, right)
        
        return left
    
    def parse_relational_expr(self) -> Expr:
        left: Expr = self.parse_add_expr()

        if (not self.end_of_tokens) and isinstance(self.current_token, RelationalOP):
            operator: str = self.current_token.op
            self.move_pointer()
            right: Expr = self.parse_relational_expr()
            return RelationalExpr(left, operator, right)
        
        return left
    
    def parse_add_expr(self) -> Expr:
        left: Expr = self.parse_modulo_expr()

        if (not self.end_of_tokens) and isinstance(self.current_token, MathOP) and self.current_token.op in '+-':
            operator: str = self.current_token.op
            self.move_pointer()
            right: Expr = self.parse_add_expr()
            return AddExpr(left, operator, right)
        
        return left
    
    def parse_modulo_expr(self) -> Expr:
        left: Expr = self.parse_mul_expr()

        if (not self.end_of_tokens) and isinstance(self.current_token, MathOP) and self.current_token.op == '%':
            self.move_pointer()
            right: Expr = self.parse_modulo_expr()
            return ModulusExpr(left, right)
        
        return left
    
    def parse_mul_expr(self) -> Expr:
        left: Expr = self.parse_unary_expr()

        if (not self.end_of_tokens) and isinstance(self.current_token, MathOP) and self.current_token.op in '*/':
            operator: str = self.current_token.op
            self.move_pointer()
            right: Expr = self.parse_mul_expr()
            return MulExpr(left, operator, right)
        
        return left
    
    def parse_unary_expr(self) -> Expr:
        if isinstance(self.current_token, NotOP):
            self.move_pointer()
            e: Expr = self.parse_unary_expr()
            return NotExpr(e)
        
        elif isinstance(self.current_token, MathOP):
            if self.current_token.op == '-':
                self.move_pointer()
                try:
                    expr: Expr = self.parse_unary_expr()
                    return NegateExpr(expr)
                except:
                    print("Syntax Error: Expected an expression after -")
                    sys.exit()
                
            
            elif self.current_token.op == '+':
                self.move_pointer()
                try:
                    e2: Expr = self.parse_unary_expr()
                    return e2
                except:
                    print("Syntax Error: Expected an expression after +")
                    sys.exit()
            else:
                print(f"Synatx Error: Can't use {self.current_token.op} as a unary operator")
                sys.exit()

        return self.parse_primary_expr()
    
    def parse_primary_expr(self) -> Expr:
        # If there is no token to work with return 0
        if (self.end_of_tokens):
            print("Syntax Error in parsing primary expressions")
            sys.exit()

        elif isinstance(self.current_token, NumberToken):
            n: NumberNode = NumberNode(self.current_token.value)
            self.move_pointer()
            return n
        
        elif isinstance(self.current_token, Identifier):
            i: IdentifierNode = IdentifierNode(self.current_token.word)
            self.move_pointer()
            return i
        
        elif isinstance(self.current_token, Boolean):
            b: BooleanNode = BooleanNode(self.current_token.value)
            self.move_pointer()
            return b
        
        elif isinstance(self.current_token, Parenthesis) and self.current_token.symbol == '(':
            self.move_pointer()
            e : Expr = self.parse_assignment()

            if not isinstance(self.current_token, Parenthesis) or self.current_token.symbol != ')':
                print("Expected a )")
                sys.exit()

            self.move_pointer()
            return e
        
        else:
            print("Invalid syntax found in the parse_primary function")
            sys.exit()