from parser import *
from lexer import *
from typing import List


class Environment:
    def __init__(self, parent=None):
        self.symbols: dict[str, float | str | bool | None] = {}
        self.parent: Optional[Environment] = parent

    def set_value(self, key: str, value: float | str | bool | None) -> None:
        self.symbols[key] = value

    def get_value(self, key: str) -> Optional[float | str | bool]:
        try: return self.symbols[key]
        except KeyError: return None

    def __contains__(self, key: str):
        return key in self.symbols
    
    def __getitem__(self, key: str):
        return self.symbols[key]


class Interpreter:
    def __init__(self):
        self.scanner: Lexer= Lexer()
        self.parser: Parser = Parser()
        
        self._global: Environment = Environment()
        self.environments: dict[ast.BlockStatement, Environment] = {}
        self.current_env: Environment = self._global

        self.repl_mode = False

        self.evaluators = {
            ast.NodeType.IDENTIFIER_NODE    : self.identifier_node, 
            ast.NodeType.BOOL_NODE          : self.bool_node,
            ast.NodeType.REAL_NODE          : self.real_node,
            
            ast.NodeType.INVERSION          : self.not_node,
            ast.NodeType.NEGATION           : self.negation,
            ast.NodeType.FACTOR             : self.factor,
            
            ast.NodeType.MODULO             : self.modulo,
            ast.NodeType.TERM               : self.term,
            ast.NodeType.COMPARISON         : self.comparison,
            
            ast.NodeType.EQUALITY           : self.equality,
            ast.NodeType.LOGICAL            : self.logical,
            ast.NodeType.ASSIGNMENT         : self.assignment,
            
            ast.NodeType.PRINT_STMT         : self.print_stmt,
            ast.NodeType.EXPR_STMT          : self.expr_stmt,
            ast.NodeType.LET_STMT           : self.let_stmt,
            ast.NodeType.IF_STMT            : self.if_stmt,
            ast.NodeType.WHILE_STMT         : self.while_stmt,
            ast.NodeType.BLOCK_STMT         : self.block_stmt,

            ast.NodeType.STRING_NODE        : self.string_node
        }

    
    def log(self, message: str) -> None:
        print("[Semantic Error] " + message)


    def repl(self) -> None:
        self.repl_mode = True

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


    def block_stmt(self, stmt: ast.BlockStatement) -> None:
        parent = self.current_env
        self.environments[stmt] = Environment(parent)
        self.current_env = self.environments[stmt]

        for s in stmt.array:
            handle = self.evaluators[s.type]
            handle(s)

        # Restore the original environment and delete the current environment
        self.current_env = parent
        del self.environments[stmt]


    def while_stmt(self, stmt: ast.WhileStatement) -> None:
        handle_expression = self.evaluators[stmt.expression.type]
        
        if stmt.primary is None:
            while bool(handle_expression(stmt.expression)):
                pass
            return
        
        handle_primary = self.evaluators[stmt.primary.type]
        while bool(handle_expression(stmt.expression)):
            handle_primary(stmt.primary)


    def if_stmt(self, stmt: ast.IfStatement) -> None:
        handle = self.evaluators[stmt.expression.type]
        condition = bool(handle(stmt.expression))

        if condition and stmt.primary:
            handle = self.evaluators[stmt.primary.type]
            handle(stmt.primary)

        elif stmt.secondary:
            handle = self.evaluators[stmt.secondary.type]
            handle(stmt.secondary)
    

    def let_stmt(self, stmt: ast.LetStatement) -> None:
        self.current_env.set_value(stmt.primary.token.lexeme, None)
        if stmt.secondary:
            value: Optional[str | float | bool] = self.execute_expr(stmt.secondary)
            self.current_env.set_value(stmt.primary.token.lexeme, value)
        return


    def expr_stmt(self, stmt: ast.ExpressionStatement) -> None:
        value = self.execute_expr(stmt.primary)
        if self.repl_mode:
            print(value)
    

    def print_stmt(self, stmt: ast.PrintStatement) -> None:
        for e in stmt.expressions:
            value = self.execute_expr(e)
            print(value, end='')
        
        print()


    def execute_expr(self, expr: ast.BinaryNode | ast.UnaryNode | ast.Node) -> float:
        handler = self.evaluators[expr.type]
        return handler(expr)


    def string_node(self, expr: ast.Node) -> str:
        return expr.token.lexeme[1:-1]


    def assignment(self, expr: ast.BinaryNode) -> float:
        ID = expr.operand[0].token.lexeme

        # Look for the variable in the scope tree
        env = self.current_env
        while env is not None:
            if ID in env:
                break
            env = env.parent

        if not env: 
            self.log(f"Variable {ID} is not defined")
            return -1
        
        value : float = self.execute_expr(expr.operand[1])
        env.set_value(ID, value)
        return value
        

    def logical(self, expr: ast.BinaryNode) -> float:
        l: float = self.execute_expr(expr.operand[0])
        r: float = self.execute_expr(expr.operand[1])

        if expr.operator.lexeme == 'and':
            return float(l and r)
        
        return float(l or r)
    
    def equality(self, expr: ast.BinaryNode) -> float:
        l: float = self.execute_expr(expr.operand[0])
        r: float = self.execute_expr(expr.operand[1])

        if expr.operator.lexeme == '==':
            return float(l == r)
        
        return float(l != r)
    
    def comparison(self, expr: ast.BinaryNode) -> float:
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
        
    def term(self, expr: ast.BinaryNode) -> float:
        l: float = self.execute_expr(expr.operand[0])
        r: float = self.execute_expr(expr.operand[1])

        if expr.operator.lexeme == '+':
            return l + r
        else:
            return l - r
        
    def modulo(self, expr: ast.BinaryNode) -> float:
        l: float = self.execute_expr(expr.operand[0])
        r: float = self.execute_expr(expr.operand[1])

        if r == 0:
            self.log("Modulo by zero")
            return -1

        return int(l) % int(r)
    
    def factor(self, expr: ast.BinaryNode) -> float:
        l: float = self.execute_expr(expr.operand[0])
        r: float = self.execute_expr(expr.operand[1])

        if expr.operator.lexeme == '*':
            return l * r
        elif r == 0:
            self.log("Division by zero")
            return -1
        else:
            return l / r
        
    def negation(self, expr: ast.UnaryNode) -> float:
        value: float = -1 * self.execute_expr(expr.operand)
        return value
    
    def not_node(self, expr: ast.UnaryNode) -> float:
        value: float = not self.execute_expr(expr.operand)
        return float(value)

    def real_node(self, n: ast.Node) -> float:
        return float(n.token.lexeme)
    
    def bool_node(self, b: ast.Node) -> float:
        value = b.token.lexeme
        return 1 if value == 'True' else 0
    
    def identifier_node(self, i: ast.Node) -> Optional[float | str | bool]:
        ID = i.token.lexeme
        env = self.current_env

        while env is not None:
            if ID in env:
                break
            env = env.parent

        if not env:
            self.log(f"Undefined variable, {i.token.lexeme}")
            return -1
        
        value = env[i.token.lexeme]
        return value
            