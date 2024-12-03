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