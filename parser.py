import sys
import syntax_tree as ast
from lexer import *
from typing import List, Tuple

class Parser:
    def __init__(self):
        self.tree: List[ast.Statement] = []
        self.index: int = 0
        self.tokens: List[Token] = []
        self.error: bool = False


    def log(self, message):
        self.error = True
        print(f"[Syntax Error] {message}, at line {self.current_token.line}")


    def synchronize(self):
        while not self.at_end:
            if self.current_token.type == TokenType.SEMICOLON:
                self.index += 1
                break
            self.index += 1

    @property
    def current_token(self) -> Token:
        return self.tokens[self.index]

    @property
    def at_end(self) -> bool:
        return self.current_token.type == TokenType.EOF


    def advance(self) -> None:
        self.index += 1


    def consume(self, t: TokenType, message: str = '') -> Optional[Token]:
        if self.current_token.type == t:
            token = self.current_token
            self.advance()
            return token
        else:
            self.log(message)
            self.synchronize()
            return None


    def consume_semicolon(self) -> Optional[Token]:
        return self.consume(TokenType.SEMICOLON, "Expected a semicolon")


    def parse(self, tokens: List[Token]) -> None:
        self.tree.clear()
        self.index = 0
        self.tokens = tokens
        self.error = False

        while not self.at_end:
            node = self.statement()
            if node:
                self.tree.append(node)


    def statement(self) -> Optional[ast.Statement]:
            
        if self.current_token.type == TokenType.PRINT:
            p: Optional[ast.PrintStatement] = self.print_statement()
            return p
        
        elif self.current_token.type == TokenType.LET:
            l: Optional[ast.LetStatement] = self.let_statement()
            return l
                    
        elif self.current_token.type == TokenType.IF:
            i: Optional[ast.IfStatement] = self.if_statement()
            return i
        
        elif self.current_token.type == TokenType.WHILE:
            w : Optional[ast.WhileStatement] = self.while_statement()
            return w
        
        elif self.current_token.type == TokenType.BRACE and self.current_token.lexeme == '{':
            b: Optional[ast.BlockStatement] = self.block_statement()
            return b
        
        e: Optional[ast.Node | ast.UnaryNode | ast.BinaryNode] = self.assignment()
        if not e:
            return None
        
        e_statement: ast.ExpressionStatement = ast.ExpressionStatement(e)
        self.consume_semicolon()
        return e_statement


    def print_statement(self) -> Optional[ast.PrintStatement]:
        self.consume(TokenType.PRINT)
        expressions : List[ast.Node | ast.UnaryNode | ast.BinaryNode] = []
        
        while not self.at_end and self.current_token.type != TokenType.SEMICOLON:
            e : Optional[ast.Node | ast.UnaryNode | ast.BinaryNode] = self.assignment()
            if e: expressions.append(e)

        self.consume_semicolon()
        return ast.PrintStatement(expressions)


    def let_statement(self) -> Optional[ast.LetStatement]:
        self.consume(TokenType.LET)
        ID : Optional[ast.Node] = self.identifier()

        if not ID:
            return None
            
        e: Optional[ast.BinaryNode | ast.UnaryNode | ast.Node] = None

        if not self.at_end and self.current_token.type == TokenType.ASSIGNMENT:
            self.consume(TokenType.ASSIGNMENT)
            e = self.assignment()
            
        self.consume_semicolon()
        return ast.LetStatement(ID, e)


    def if_statement(self) -> Optional[ast.IfStatement]:
        self.consume(TokenType.IF)

        e: Optional[ast.BinaryNode | ast.UnaryNode | ast.Node] = self.assignment()
        if not e:
            self.log("Expected an expression after 'if' keyword")
            self.synchronize()
            return None
        
        if not self.consume(TokenType.THEN, "Expected a 'then' after if statement"):
            return None

        p: Optional[ast.Statement] = self.statement()
        q: Optional[ast.Statement] = None

        if self.current_token.type == TokenType.ELSE:
            self.consume(TokenType.ELSE)
            q = self.statement()

        return ast.IfStatement(p, e, q)
    

    def while_statement(self) -> Optional[ast.WhileStatement]:
        self.consume(TokenType.WHILE)
        
        e : Optional[ast.BinaryNode | ast.UnaryNode | ast.Node] = self.assignment()
        if not e:
            self.log("Expected an expression after 'while' keyword")
            self.synchronize()
            return None
        
        if not self.consume(TokenType.DO, "Expected a 'do' after while statement"):
            return None
        
        s: Optional[ast.Statement] = self.statement()
        return ast.WhileStatement(s, e)
    
    def block_statement(self) -> Optional[ast.BlockStatement]:
        self.consume(TokenType.BRACE)
        array : List[ast.Statement] = []

        while not self.at_end and self.current_token.lexeme != '}':
            s: Optional[ast.Statement] = self.statement()
            if s: array.append(s)

        if not self.consume(TokenType.BRACE, "Unterminated block, expected a '}'"):
            return None
        
        node = ast.BlockStatement(array)
        return node

    def assignment(self) -> Optional[ast.BinaryNode | ast.UnaryNode | ast.Node]:
        lvalue: Optional[ast.BinaryNode | ast.UnaryNode | ast.Node] = self.logical()

        if not lvalue:
            return None

        if self.current_token.type == TokenType.ASSIGNMENT:
            op = self.consume(TokenType.ASSIGNMENT)
            
            if op and lvalue.type == ast.NodeType.IDENTIFIER_NODE:
                rvalue: Optional[ast.BinaryNode | ast.UnaryNode | ast.Node] = self.assignment()
                if not rvalue:
                    self.log("Expected an expression after =")
                    self.synchronize()
                    return None
                  
                return ast.BinaryNode(ast.NodeType.ASSIGNMENT, op, lvalue, rvalue)

            else:
                self.log("Expected an identifier before =")
                self.synchronize()
                return None
        
        return lvalue
        

    def logical(self) -> Optional[ast.BinaryNode | ast.UnaryNode | ast.Node]:
        l: Optional[ast.BinaryNode | ast.UnaryNode | ast.Node] = self.equality()

        if not l:
            return None
        
        if not self.at_end and self.current_token.type == TokenType.LOGICAL_OP:
            operator: Token = self.current_token
            self.advance()
            r: Optional[ast.BinaryNode | ast.UnaryNode | ast.Node ] = self.logical()

            if not r:
                self.log(f"Expected an expression after {operator.lexeme} operator")
                self.synchronize()
                return None

            return ast.BinaryNode(ast.NodeType.LOGICAL, operator, l, r)
        return l
    
    def equality(self) ->  Optional[ast.BinaryNode | ast.UnaryNode | ast.Node]:
        l: Optional[ast.BinaryNode | ast.UnaryNode | ast.Node] = self.comparison()

        if not l:
            return None
        
        if not self.at_end and (self.current_token.type == TokenType.EQUALITY_OP or self.current_token.type == TokenType.INEQUALITY_OP):
            operator: Token = self.current_token
            self.advance()
            r: Optional[ast.BinaryNode | ast.UnaryNode | ast.Node ] = self.equality()

            if not r:
                self.log(f"Expected an expression after {operator.lexeme} operator")
                self.synchronize()
                return None

            return ast.BinaryNode(ast.NodeType.EQUALITY, operator, l, r)
        return l
    
    
    def comparison(self) -> Optional[ast.BinaryNode | ast.UnaryNode | ast.Node]:
        l: Optional[ast.BinaryNode | ast.UnaryNode | ast.Node] = self.term()

        if not l:
            return None
        
        if not self.at_end and self.current_token.type == TokenType.RELATIONAL_OP:
            operator: Token = self.current_token
            self.advance()
            r: Optional[ast.BinaryNode | ast.UnaryNode | ast.Node ] = self.comparison()

            if not r:
                self.log(f"Expected an expression after {operator.lexeme} operator")
                self.synchronize()
                return None

            return ast.BinaryNode(ast.NodeType.COMPARISON, operator, l, r)
        
        return l
    
    def term(self) -> Optional[ast.BinaryNode | ast.UnaryNode | ast.Node]:
        l: Optional[ast.BinaryNode | ast.UnaryNode | ast.Node] = self.modulo()

        if not l:
            return None
        
        if not self.at_end and self.current_token.type == TokenType.ARITHMETIC_OP and self.current_token.lexeme in '+-':
            operator: Token = self.current_token
            self.advance()
            r: Optional[ast.BinaryNode | ast.UnaryNode | ast.Node ] = self.term()

            if not r:
                self.log(f"Expected an expression after {operator.lexeme} operator")
                self.synchronize()
                return None

            return ast.BinaryNode(ast.NodeType.TERM, operator, l, r)
        return l
    
    def modulo(self) -> Optional[ast.BinaryNode | ast.UnaryNode | ast.Node]:
        l: Optional[ast.BinaryNode | ast.UnaryNode | ast.Node] = self.factor()

        if not l:
            return None
        
        if not self.at_end and self.current_token.type == TokenType.ARITHMETIC_OP and self.current_token.lexeme in '%':
            operator: Token = self.current_token
            self.advance()
            r: Optional[ast.BinaryNode | ast.UnaryNode | ast.Node ] = self.modulo()

            if not r:
                self.log(f"Expected an expression after {operator.lexeme} operator")
                self.synchronize()
                return None

            return ast.BinaryNode(ast.NodeType.MODULO, operator, l, r)
        return l
    
    def factor(self) -> Optional[ast.BinaryNode | ast.UnaryNode | ast.Node]:
        l: Optional[ast.BinaryNode | ast.UnaryNode | ast.Node] = self.unary()

        if not l:
            return None
        
        if not self.at_end and self.current_token.type == TokenType.ARITHMETIC_OP and self.current_token.lexeme in '*/':
            operator: Token = self.current_token
            self.advance()
            r: Optional[ast.BinaryNode | ast.UnaryNode | ast.Node ] = self.factor()

            if not r:
                self.log(f"Expected an expression after {operator.lexeme} operator")
                self.synchronize()
                return None

            return ast.BinaryNode(ast.NodeType.FACTOR, operator, l, r)
        return l
    
    def unary(self) -> Optional[ast.BinaryNode | ast.UnaryNode | ast.Node]:
        prefix: Token = self.current_token

        if prefix.type == TokenType.NOT_OP or prefix.type == TokenType.ARITHMETIC_OP:
            self.advance()
            operand: Optional[ast.BinaryNode | ast.UnaryNode | ast.Node] = self.unary()
            if not operand:
                self.log(f"Expected an expression after {prefix.lexeme} operator")
                self.synchronize()
                return None
            
            if prefix.type == TokenType.NOT_OP:
                return ast.UnaryNode(ast.NodeType.INVERSION, operand)
            
            if prefix.lexeme == '-':
                return ast.UnaryNode(ast.NodeType.NEGATION, operand)
            elif prefix.lexeme == '+':
                return operand
            else:
                self.log(f"Invalid unary operator, {prefix.lexeme}")
                self.synchronize()
                return None
            
        return self.primary()
      

    def primary(self) -> Optional[ast.BinaryNode | ast.UnaryNode | ast.Node]:
        if self.current_token.type ==  TokenType.REAL:
            r: ast.Node = ast.Node(ast.NodeType.REAL_NODE, self.current_token)
            self.advance()
            return r
        
        elif self.current_token.type == TokenType.STRING:
            s: ast.Node = ast.Node(ast.NodeType.STRING_NODE, self.current_token)
            self.advance()
            return s
        
        elif self.current_token.type == TokenType.IDENTIFIER:
            i: ast.Node | None = self.identifier()
            return i
        
        elif self.current_token.type == TokenType.BOOLEAN:
            b: ast.Node = ast.Node(ast.NodeType.BOOL_NODE, self.current_token)
            self.advance()
            return b
        
        elif self.current_token.type == TokenType.PARENTHESIS and self.current_token.lexeme == '(':
            self.advance()
            e: Optional[ast.BinaryNode | ast.UnaryNode | ast.Node] = self.assignment()

            if not (self.current_token.type == TokenType.PARENTHESIS and self.current_token.lexeme == ')'):
                self.log("Unterminated parenthesis")
                self.synchronize()

            self.advance()
            return e
        
        self.log("Invalid syntax")
        self.synchronize()
        return None
    
    
    def identifier(self) -> Optional[ast.Node]:
        lexeme = self.current_token.lexeme
        if self.current_token.type == TokenType.IDENTIFIER:
            if lexeme in Reserved.keys():
                self.log(f"'{lexeme}' is a reserverd keyword")
                self.synchronize()
                return None
            else:
                token = self.current_token
                self.advance()
                return ast.Node(ast.NodeType.IDENTIFIER_NODE, token)
            
        self.log("expected an identifier")
        self.synchronize()
        return None 