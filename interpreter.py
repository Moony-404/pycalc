from parser import *
from scanner import *
from typing import List

class Interpreter:
    def __init__(self):
        self.scanner: Lexer= Lexer()
        self.parser: Parser = Parser()
        self.symbols: dict = {}
        
        self.exec_functions = [
            self.execute_identifier_node, 
            self.execute_bool_node,
            self.execute_number_node,
            
            self.execute_not_expr,
            self.execute_negate_expr,
            self.execute_mul_expr,
            
            self.execute_modulus_expr,
            self.execute_add_expr,
            self.execute_relational_expr,
            
            self.execute_equality_expr,
            self.execute_logical_expr,
            self.execute_assignment_expr,
            
            self.execute_print_stmt,
            self.execute_expr_stmt,
            self.execute_let_stmt,
            self.execute_if_stmt
        ]

    def repl(self) -> None:
        while (True):
            user_input: str = input("> ")
            user_input = user_input.strip()
            if user_input == 'exit' or user_input == 'quit':
                break

            self.scanner.scan(user_input)
            if self.scanner.error:
                continue

            self.parser.parse(self.scanner.tokens)
            if self.parser.error:
                continue
                        
            self.execute(self.parser.tree)

    def run(self, source: str) -> None:
        self.scanner.scan(source)
        if self.scanner.error:
            return
        
        self.parser.parse(self.scanner.tokens)
        if self.parser.error:
            return
        
        self.execute(self.parser.tree)

    def execute(self, script: List[ast.Stmt]) -> None:
        for stmt in script:
            ID = stmt.AST_ID
            if ID == -1:
                print(f"[Error] Invalid statement")
                continue

            handler = self.exec_functions[ID]
            handler(stmt)

    def execute_if_stmt(self, stmt: ast.IfStmt) -> None:
        handle = self.exec_functions[stmt.condition.AST_ID]
        condition = bool(handle(stmt.condition))

        if condition and stmt.true_stmt:
            handle = self.exec_functions[stmt.true_stmt.AST_ID]
            handle(stmt.true_stmt)

        elif stmt.false_stmt:
            handle = self.exec_functions[stmt.false_stmt.AST_ID]
            handle(stmt.false_stmt)
    
    def execute_let_stmt(self, stmt: ast.LetStmt) -> None:
        if stmt.expr is None:
            return None
        value: float = self.execute_expr(stmt.expr)
        self.symbols[stmt.name] = value

    def execute_expr_stmt(self, stmt: ast.ExprStmt) -> None:
        value = self.execute_expr(stmt.expr)
    
    def execute_print_stmt(self, stmt: ast.PrintStmt) -> None:
        value = self.execute_expr(stmt.expr)
        print(value)

    def execute_expr(self, expr: ast.Expr) -> float:
        ID = expr.AST_ID
        if ID == -1:
            print(f"[Error] Invalid Expression")

        handler = self.exec_functions[ID]
        return handler(expr)

    def execute_assignment_expr(self, assign: ast.Assignment) -> float:
        if assign.word in self.symbols:
            value : float = self.execute_expr(assign)
            self.symbols[assign.word] = value
            return value
        
        print(f"[Error] Variable {assign.word} does not exist")
        return 0

    def execute_logical_expr(self, expr: ast.LogicalExpr) -> float:
        l: float = self.execute_expr(expr.left)
        r: float = self.execute_expr(expr.right)

        if expr.operator == 'and':
            return float(l and r)
        
        return float(l or r)
    
    def execute_equality_expr(self, expr: ast.EqualityExpr) -> float:
        l: float = self.execute_expr(expr.left)
        r: float = self.execute_expr(expr.right)

        if expr.operator == '==':
            return float(l == r)
        
        return float(l != r)
    
    def execute_relational_expr(self, expr: ast.RelationalExpr) -> float:
        l: float = self.execute_expr(expr.left)
        r: float = self.execute_expr(expr.right)

        if expr.operator == '<':
            return float(l < r)
        elif expr.operator == '<=':
            return float(l <= r)
        elif expr.operator == '>':
            return float(l > r)
        else:
            return float(l >= r)
        
    def execute_add_expr(self, expr: ast.AddExpr) -> float:
        l: float = self.execute_expr(expr.left)
        r: float = self.execute_expr(expr.right)

        if expr.operator == '+':
            return l + r
        else:
            return l - r
        
    def execute_modulus_expr(self, expr: ast.ModulusExpr) -> float:
        l: float = self.execute_expr(expr.left)
        r: float = self.execute_expr(expr.right)

        return int(l) % int(r)
    
    def execute_mul_expr(self, expr: ast.MulExpr) -> float:
        l: float = self.execute_expr(expr.left)
        r: float = self.execute_expr(expr.right)

        if expr.operator == '*':
            return l * r
        elif r == 0:
            print("Error: Division by Zero")
            sys.exit()
        else:
            return l / r
        
    def execute_negate_expr(self, expr: ast.NegateExpr) -> float:
        value: float = -1 * self.execute_expr(expr.expr)
        return value
    
    def execute_not_expr(self, expr: ast.NotExpr) -> float:
        value: float = not self.execute_expr(expr.expr)
        return float(value)

    def execute_number_node(self, n: ast.NumberNode) -> float:
        return n.value
    
    def execute_bool_node(self, b: ast.BooleanNode) -> float:
        return float(b.value)
    
    def execute_identifier_node(self, iden: ast.IdentifierNode) -> float:
        try:
            value = self.symbols[iden.word]
            return value
        except KeyError:
            print(f"[Error] Undefined variable '{iden.word}'")
            return 0