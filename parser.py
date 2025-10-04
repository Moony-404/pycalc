from __future__ import annotations
import sys
import syntax_tree as ast
from scanner import *
from typing import List

class Parser:
    def __init__(self):
        self.script: List[ast.Stmt] = []
        self.index: int = 0
        self.tokens: List[Token] = []
        self.error = False

    def log(self, message):
        self.error = True
        print(f"[Syntax Error] {message} : {self.current_token.line}")

    def synchronize(self):
        while not self.end_of_tokens:
            if self.current_token.type == TokenType.SEMICOLON:
                self.index += 1
                break
            self.index += 1

    @property
    def current_token(self) -> Token:
        return self.tokens[self.index]

    @property
    def end_of_tokens(self) -> bool:
        return self.current_token.type == TokenType.EOF

    def move_pointer(self) -> None:
        self.index += 1

    def consume(self, t: TokenType, message: str = '') -> None:
        if self.current_token.type == t:
            self.move_pointer()

        else:
            self.log(message)
            self.synchronize()

    def consume_semicolon(self) -> None:
        self.consume(TokenType.SEMICOLON, "Expected a semicolon")

    def parse(self, tokens: List[Token]) -> None:
        self.script = []
        self.index = 0
        self.tokens = tokens
        self.error = False

        while not self.end_of_tokens:
            node = self.parse_stmt()
            if node is not None:
                self.script.append(node)

        if not self.end_of_tokens:
            self.log("Invalid syntax, unnecessay tokens")

    def parse_stmt(self) -> Optional[ast.Stmt]:
        if self.current_token.type == TokenType.IDENTIFIER:
            if  self.current_token.lexeme == 'print':
                print_stmt : ast.Stmt = self.parse_print_stmt()
                return print_stmt
            
            elif self.current_token.lexeme == 'let':
                let_stmt = self.parse_let_stmt()
                return let_stmt
        
        expr : ast.Expr = self.parse_assignment()
        expr_stmt : ast.ExprStmt = ast.ExprStmt(expr)
        self.consume_semicolon()
        
        return expr_stmt

    def parse_print_stmt(self) -> ast.PrintStmt:
        self.move_pointer()
        e : ast.Expr = self.parse_assignment()
        self.consume_semicolon()
        return ast.PrintStmt(e)
    
    def parse_let_stmt(self) -> Optional[ast.LetStmt]:
        self.move_pointer()
        if self.current_token.type == TokenType.IDENTIFIER:
            name = self.current_token.lexeme
            self.move_pointer()
        else:
            self.log("Expected an identifier after let")
            self.synchronize()
            return 
        
        e: Optional[ast.Expr] = None

        if not self.end_of_tokens and self.current_token.type == TokenType.ASSIGNMENT:
            self.move_pointer()
            e: Optional[ast.Expr] = self.parse_assignment()
            
        self.consume_semicolon()
        return ast.LetStmt(name, e)

    def parse_assignment(self) -> ast.Expr:
        lvalue: ast.Expr = self.parse_logical_expr()

        if not self.end_of_tokens and self.current_token.type == TokenType.ASSIGNMENT and isinstance(lvalue, ast.IdentifierNode):
            self.move_pointer()
            rvalue: ast.Expr = self.parse_logical_expr()
            return ast.Assignment(lvalue.word, rvalue)
        
        return lvalue
    
    def parse_logical_expr(self) -> ast.Expr:
        left: ast.Expr = self.parse_equality_expr()

        if not self.end_of_tokens and self.current_token.type == TokenType.LOGICAL_OP:
            operator: str = self.current_token.lexeme
            self.move_pointer()
            right: ast.Expr = self.parse_logical_expr()
            return ast.LogicalExpr(left, operator, right)
        
        return left
    
    def parse_equality_expr(self) -> ast.Expr:
        left: ast.Expr = self.parse_relational_expr()

        if not self.end_of_tokens and self.current_token.type == TokenType.EQUALITY_OP:
            operator: str = self.current_token.lexeme
            self.move_pointer()
            right: ast.Expr = self.parse_equality_expr()
            return ast.EqualityExpr(left, operator, right)
        
        return left
    
    def parse_relational_expr(self) -> ast.Expr:
        left: ast.Expr = self.parse_add_expr()

        if not self.end_of_tokens and self.current_token.type == TokenType.RELATIONAL_OP:
            operator: str = self.current_token.lexeme
            self.move_pointer()
            right: ast.Expr = self.parse_relational_expr()
            return ast.RelationalExpr(left, operator, right)
        
        return left
    
    def parse_add_expr(self) -> ast.Expr:
        left: ast.Expr = self.parse_modulo_expr()

        if not self.end_of_tokens and self.current_token.type == TokenType.ARITHMETIC_OP and self.current_token.lexeme in '+-':
            operator: str = self.current_token.lexeme
            self.move_pointer()
            right: ast.Expr = self.parse_add_expr()
            return ast.AddExpr(left, operator, right)
        
        return left
    
    def parse_modulo_expr(self) -> ast.Expr:
        left: ast.Expr = self.parse_mul_expr()

        if not self.end_of_tokens and self.current_token.type == TokenType.ARITHMETIC_OP and self.current_token.lexeme == '%':
            self.move_pointer()
            right: ast.Expr = self.parse_modulo_expr()
            return ast.ModulusExpr(left, right)
        
        return left
    
    def parse_mul_expr(self) -> ast.Expr:
        left: ast.Expr = self.parse_unary_expr()

        if not self.end_of_tokens and self.current_token.type == TokenType.ARITHMETIC_OP and self.current_token.lexeme in '*/':
            operator: str = self.current_token.lexeme
            self.move_pointer()
            right: ast.Expr = self.parse_mul_expr()
            return ast.MulExpr(left, operator, right)
        
        return left
    
    def parse_unary_expr(self) -> ast.Expr:
        if self.current_token.type == TokenType.NOT_OP:
            self.move_pointer()
            e = self.parse_unary_expr()
            return ast.NotExpr(e)
        
        elif self.current_token.type == TokenType.ARITHMETIC_OP:
            if self.current_token.lexeme == '-':
                self.move_pointer()
                try:
                    expr = self.parse_unary_expr()
                    return ast.NegateExpr(expr)
                except:
                    print("Syntax Error: Expected an expression after -")
                    sys.exit()
                
            
            elif self.current_token.lexeme == '+':
                self.move_pointer()
                try:
                    e2: ast.Expr = self.parse_unary_expr()
                    return e2
                except:
                    print("Syntax Error: Expected an expression after +")
                    sys.exit()
            else:
                print(f"Synatx Error: Can't use {self.current_token.lexeme} as a unary operator")
                sys.exit()

        return self.parse_primary_expr()
    
    def parse_primary_expr(self) -> ast.Expr:
        # If there is no token to work with return 0
        if (self.end_of_tokens):
            print("Syntax Error in parsing primary expressions")
            sys.exit()

        elif self.current_token.type ==  TokenType.REAL:
            n: ast.NumberNode = ast.NumberNode(float(self.current_token.lexeme))
            self.move_pointer()
            return n
        
        elif self.current_token.type == TokenType.IDENTIFIER:
            i: ast.IdentifierNode = ast.IdentifierNode(self.current_token.lexeme)
            self.move_pointer()
            return i
        
        elif self.current_token.type == TokenType.BOOLEAN:
            b: ast.BooleanNode = ast.BooleanNode(bool(self.current_token.lexeme))
            self.move_pointer()
            return b
        
        elif self.current_token.type == TokenType.PARENTHESIS and self.current_token.lexeme == '(':
            self.move_pointer()
            e : ast.Expr = self.parse_assignment()

            if not self.current_token.type == TokenType.PARENTHESIS or self.current_token.lexeme != ')':
                self.log("Expected a ')'")
                self.synchronize()

            self.move_pointer()
            return e
        
        else:
            self.log("Invalid syntax")
            self.synchronize()
            sys.exit()