import sys

# Tokens for the scanner
class Token:
    def __init__(self, repr: str):
        self.repr = repr
        
    def __repr__(self):
        return f"{self.repr}"

    def __str__(self):
        return f"{self.repr}"

class LiteralToken(Token):  
    def __init__(self, value: float):
        super().__init__(str(value))
        self.value = value

class OperatorToken(Token):
    def __init__(self, op: str):
        super().__init__(op)
        self.op = op

class ParenToken(Token):
    def __init__(self, paren):
        super().__init__(paren)
        self.paren = paren

class Scanner:

    numbers = '0123456789.'
    operators = '+-*/'
    parenthesis = '()'
    whitespaces = ' \t\n'

    def __init__(self):
        self.tokens = []
        self.string = ''
        self.index = 0

    def scan(self, string):

        self.string = string
        self.index = 0
        self.tokens = []

        while self.inside_string():
            if self.current_char in Scanner.numbers:
                self.scan_nums()
            elif self.current_char in Scanner.operators:
                self.scan_ops()
            elif self.current_char in Scanner.whitespaces:
                self.index += 1
            elif self.current_char in Scanner.parenthesis:
                self.scan_parens()
            else:
                print("Invalid syntax")
                return

    def inside_string(self):
        return self.index < len(self.string)

    @property
    def current_char(self):
        return self.string[self.index]
    
    def scan_nums(self):
        number = '' 
        decimal_flag = True
        while (self.inside_string() and self.current_char in Scanner.numbers):

            if (self.current_char == '.' and decimal_flag):
                decimal_flag = False
            
            elif (self.current_char == '.' and not decimal_flag):
                print("Syntax Error: Two decimals in a number")
                sys.exit()
                
            number += self.current_char
            self.index += 1

        self.tokens.append(LiteralToken(float(number)))

    def scan_ops(self):
        self.tokens.append(OperatorToken(self.current_char))
        self.index += 1

    def scan_parens(self):
        self.tokens.append(ParenToken(self.current_char))
        self.index += 1

# Nodes of the AST created by Recursive Descent Parsing
class BinaryNode:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def evaluate(self):
        l = self.left.evaluate()
        r = self.right.evaluate()
        
        if self.operator == '+':
            return l + r
        elif self.operator == '-':
            return l - r
        elif self.operator == '*':
            return l * r
        elif self.operator == '/':
            if (r == 0):
                print("Divide by zero error.")
                sys.exit() 
            return l / r
        
class LiteralNode:
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

# Finally the recursive descent parser
# I am turning the parser into its own class just so that I can handle all the internal states. 
# There is no reason why I couldn't have done this with simple functions 

class Parser:
    def __init__(self):
        self.ast = None

        # index related to the list of tokens
        self.index = 0
        self.tokens = []

    @property
    def current_token(self):
        return self.tokens[self.index]

    @property
    def end_of_tokens(self):
        return (True if self.index >= len(self.tokens) else False)

    def move_pointer(self):
        self.index += 1

    def parse(self, tokens):
        # Initialize the state of the parser
        self.tokens = tokens
        self.index = 0
        self.ast = None

        expr = self.parse_expr()

        self.ast = expr

    def evaluate(self):
        return self.ast.evaluate()

    def parse_expr(self):
        left = self.parse_factors()

        if (not self.end_of_tokens) and isinstance(self.current_token, OperatorToken) and self.current_token.op in '+-':
            operator = self.current_token.op
            self.move_pointer()
            right = self.parse_expr()

            return BinaryNode(left, operator, right)

        return left
        
    def parse_factors(self):
        left = self.parse_terms()
        
        if (not self.end_of_tokens) and isinstance(self.current_token, OperatorToken) and self.current_token.op in '*/':
            operator = self.current_token.op
            self.move_pointer()
            right = self.parse_factors()

            return BinaryNode(left, operator, right)

        return left

    def parse_terms(self):

        # If we reached the end of list of tokens
        if (self.end_of_tokens):
            return LiteralNode(0)

        if isinstance(self.current_token, LiteralToken):
            node = LiteralNode(self.current_token.value)
            self.move_pointer()
            return node

        elif isinstance(self.current_token, OperatorToken) and self.current_token.op == '-':
            self.move_pointer()
            node = self.parse_terms()
            value = -1 * node.evaluate()
            return LiteralNode(value)

        elif isinstance(self.current_token, ParenToken) and self.current_token.paren == '(':
            self.move_pointer()
            node = self.parse_expr()

            if (not isinstance(self.current_token, ParenToken)) or (self.current_token.paren != ')'):
                print("Expected a ')'")
                sys.exit()
        
            self.move_pointer()
            return node

        else:
            print("Invalid Syntax in parse_terms")
            sys.exit()


def main():
    s = Scanner()
    p = Parser()
    while (True):
        expr = input("> ")
        if expr == 'exit' or expr == 'quit':
            break
        s.scan(expr)
        p.parse(s.tokens)
        
        print(p.evaluate())

if __name__ == "__main__":
    main()