from parser import *
from scanner import *
from typing import List

class Interpreter:
    def __init__(self):
        self.scanner: Lexer= Lexer()
        self.parser: Parser = Parser()
        self.symbols: dict = {}

        self.evaluators = {
            ast.NodeType.IDENTIFIER_NODE : self.execute_identifier_node, 
            ast.NodeType.BOOL_NODE: self.execute_bool_node,
            ast.NodeType.REAL_NODE : self.execute_real_node,
            
            ast.NodeType.INVERSION : self.execute_not_expr,
            ast.NodeType.NEGATION : self.execute_negate_expr,
            ast.NodeType.FACTOR : self.execute_mul_expr,
            
            ast.NodeType.MODULO : self.execute_modulus_expr,
            ast.NodeType.TERM : self.execute_add_expr,
            ast.NodeType.COMPARISON : self.execute_relational_expr,
            
            ast.NodeType.EQUALITY : self.execute_equality_expr,
            ast.NodeType.LOGICAL : self.execute_logical_expr,
            ast.NodeType.ASSIGNMENT : self.execute_assignment_expr,
            
            ast.NodeType.PRINT_STMT : self.execute_print_stmt,
            ast.NodeType.EXPR_STMT : self.execute_expr_stmt,
            ast.NodeType.LET_STMT : self.execute_let_stmt,
            ast.NodeType.IF_STMT : self.execute_if_stmt
        }

    
    def log(self, message: str) -> None:
        print("[Semantic Error]" + message)


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


    def execute(self, script: List[ast.Statement]) -> None:
        for stmt in script:
            handler = self.evaluators[stmt.type]
            handler(stmt)


    def execute_if_stmt(self, stmt: ast.IfStatement) -> None:
        handle = self.evaluators[stmt.expression.type]
        condition = bool(handle(stmt.expression))

        if condition and stmt.primary:
            handle = self.evaluators[stmt.primary.type]
            handle(stmt.primary)

        elif stmt.secondary:
            handle = self.evaluators[stmt.secondary.type]
            handle(stmt.secondary)
    

    def execute_let_stmt(self, stmt: ast.LetStatement) -> None:
        self.symbols[stmt.primary.token.lexeme] = None
        if stmt.secondary:
            value: float = self.execute_expr(stmt.secondary)
            self.symbols[stmt.primary.token.lexeme] = value
        return


    def execute_expr_stmt(self, stmt: ast.ExpressionStatement) -> None:
        value = self.execute_expr(stmt.primary)
    

    def execute_print_stmt(self, stmt: ast.PrintStatement) -> None:
        value = self.execute_expr(stmt.primary)
        print(value)

    def execute_expr(self, expr: ast.BinaryNode | ast.UnaryNode | ast.Node) -> float:
        handler = self.evaluators[expr.type]
        return handler(expr)

    def execute_assignment_expr(self, expr: ast.BinaryNode) -> float:
        ID = expr.operand[0].token.lexeme
        if ID in self.symbols:
            value : float = self.execute_expr(expr.operand[1])
            self.symbols[ID] = value
            return value
        
        # Need to change this
        self.log(f"Variable {ID} is not defined")
        return -1

    def execute_logical_expr(self, expr: ast.BinaryNode) -> float:
        l: float = self.execute_expr(expr.operand[0])
        r: float = self.execute_expr(expr.operand[1])

        if expr.operator.lexeme == 'and':
            return float(l and r)
        
        return float(l or r)
    
    def execute_equality_expr(self, expr: ast.BinaryNode) -> float:
        l: float = self.execute_expr(expr.operand[0])
        r: float = self.execute_expr(expr.operand[1])

        if expr.operator.lexeme == '==':
            return float(l == r)
        
        return float(l != r)
    
    def execute_relational_expr(self, expr: ast.BinaryNode) -> float:
        l: float = self.execute_expr(expr.operand[0])
        r: float = self.execute_expr(expr.operand[1])

        if expr.operator.lexeme == '<':
            return float(l < r)
        elif expr.operator.lexeme == '<=':
            return float(l <= r)
        elif expr.operator.lexeme == '>':
            return float(l > r)
        else:
            return float(l >= r)
        
    def execute_add_expr(self, expr: ast.BinaryNode) -> float:
        l: float = self.execute_expr(expr.operand[0])
        r: float = self.execute_expr(expr.operand[1])

        if expr.operator.lexeme == '+':
            return l + r
        else:
            return l - r
        
    def execute_modulus_expr(self, expr: ast.BinaryNode) -> float:
        l: float = self.execute_expr(expr.operand[0])
        r: float = self.execute_expr(expr.operand[1])

        return int(l) % int(r)
    
    def execute_mul_expr(self, expr: ast.BinaryNode) -> float:
        l: float = self.execute_expr(expr.operand[0])
        r: float = self.execute_expr(expr.operand[1])

        if expr.operator.lexeme == '*':
            return l * r
        elif r == 0:
            self.log("Division by Zero")
            return -1
        else:
            return l / r
        
    def execute_negate_expr(self, expr: ast.UnaryNode) -> float:
        value: float = -1 * self.execute_expr(expr.operand)
        return value
    
    def execute_not_expr(self, expr: ast.UnaryNode) -> float:
        value: float = not self.execute_expr(expr.operand)
        return float(value)

    def execute_real_node(self, n: ast.Node) -> float:
        return float(n.token.lexeme)
    
    def execute_bool_node(self, b: ast.Node) -> float:
        value = b.token.lexeme
        return 1 if value == 'true' else 0
    
    def execute_identifier_node(self, i: ast.Node) -> float:
        try:
            value = self.symbols[i.token.lexeme]
            return value
        except KeyError:
            self.log(f"Undefined variable, {i.token.lexeme}")
            return -1