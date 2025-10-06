from _token import *
from typing import List, Optional

class Lexer:

    NUMBERS:        str = '0123456789.'
    ARITHMETIC:     str = '+-*/%'
    RELATIONAL:     str = '<>'
    NOT:            str = '!'
    PARENTHESIS:    str = '()'
    BRACES:         str = '{}'
    WS:             str = '\t '

    def __init__(self):
        self.tokens: List[Token] = []
        self.source: str = ''
        self.index: int = 0
        self.line = 1
        self.error = False


    def log(self, message: str) -> None:
        self.error = True
        print(f"[Lexical Error] {message}, at line {self.line}")


    def synchronize(self, alphabet: str, discard = True) -> None: 
        while self.inside_source():
            condition = self.current_char in alphabet
            condition = not condition if discard else condition
            if condition:
                break
            self.index += 1
        
 
    def scan(self, text: str) -> None:
        self.tokens.clear()
        self.source = text
        self.index = 0
        self.line = 1
        self.error = False

        while self.inside_source():
            if self.current_char in Lexer.NUMBERS:
                self.scan_number()  
            
            elif self.current_char == '"':
                self.scan_string() 
            
            elif self.current_char.isalpha():
                self.scan_identifier() 

            elif self.current_char in Lexer.ARITHMETIC:
                self.scan_arithmetic_operator()

            elif self.current_char in Lexer.RELATIONAL:
                self.scan_relational_operator()
            
            elif self.current_char in Lexer.NOT:
                self.scan_not_operator()

            elif self.current_char in Lexer.PARENTHESIS:
                self.scan_parenthesis() 
            
            elif self.current_char == '=':
                self.scan_equal_symbol() 
            
            elif self.current_char in Lexer.WS:
                self.index += 1 
            
            elif self.current_char in Lexer.BRACES:
                self.scan_brace() 
            
            elif self.current_char == ';':
                self.scan_semicolon()

            elif self.current_char == ':':
                self.scan_colon()
            
            elif self.current_char == '\n':
                self.line += 1
                self.index += 1
            
            else:
                self.log("Unknown symbol")
                self.synchronize(Lexer.WS + '\n', discard = False)

        self.tokens.append(Token(TokenType.EOF, self.index, 0, self.source, self.line))


    def inside_source(self) -> bool:
        return self.index < len(self.source)

    @property
    def current_char(self) -> str:
        return self.source[self.index]
    

    def peek(self) -> Optional[str]:
        try:
            next_char: str = self.source[self.index + 1]
            return next_char
        except IndexError:
            return None


    def scan_brace(self) -> None:
        t : Token = Token(TokenType.BRACE, self.index, 1, self.source, self.line)
        self.tokens.append(t)
        self.index += 1


    def scan_semicolon(self) -> None:
        t : Token = Token(TokenType.SEMICOLON, self.index, 1, self.source, self.line)
        self.tokens.append(t)
        self.index += 1


    def scan_colon(self) -> None:
        t : Token = Token(TokenType.COLON, self.index, 1, self.source, self.line)
        self.tokens.append(t)
        self.index += 1


    def scan_identifier(self) -> None:
        start: int = self.index
        while self.inside_source() and (self.current_char.isalnum() or self.current_char == '_'):
            self.index += 1

        t: Token = Token(TokenType.IDENTIFIER, start, self.index - start, self.source, self.line)
        # word = self.source[start: self.index]
        word = t.lexeme

        for keyword in Reserved.keys():
            if word == keyword:
                t.type = Reserved[keyword]
                break

        self.tokens.append(t)


    def scan_number(self) -> None:
        start: int = self.index
        decimal_count: int = 0
        
        while self.inside_source() and self.current_char in Lexer.NUMBERS:
            if self.current_char == '.':
                decimal_count += 1

            self.index += 1

        if decimal_count > 1:
            self.log("Invalid number")
            self.synchronize(Lexer.NUMBERS)
            return   
        
        t: Token = Token(TokenType.REAL, start, self.index - start, self.source, self.line)
        self.tokens.append(t)


    def scan_string(self) -> None:
        start = self.index  
        self.index += 1

        while self.inside_source() and self.current_char != '"':
            self.index += 1

        if self.current_char == '"':
            self.index += 1
            t : Token = Token(TokenType.STRING, start, self.index - start, self.source, self.line)
            self.tokens.append(t)

        else:
            # No need to synchronize since we are at the end of file
            self.log("Unterminated string literal")


    def scan_arithmetic_operator(self) -> None:
        t : Token = Token(TokenType.ARITHMETIC_OP, self.index, 1, self.source, self.line)
        self.tokens.append(t)
        self.index += 1


    def scan_relational_operator(self) -> None:
        
        if self.peek() == '=':
            t: Token = Token(TokenType.RELATIONAL_OP, self.index, 2, self.source, self.line)
            self.tokens.append(t)
            self.index += 2
        else:
            t : Token = Token(TokenType.RELATIONAL_OP, self.index, 1, self.source, self.line)
            self.tokens.append(t)
            self.index += 1


    def scan_not_operator(self) -> None:
        if self.peek() == '=':
            t: Token = Token(TokenType.NOT_OP, self.index, 2, self.source, self.line)
            self.tokens.append(t)
            self.index += 2
        else:
            self.log("Invalid opeartor !")


    def scan_parenthesis(self) -> None:
        t: Token = Token(TokenType.PARENTHESIS, self.index, 1, self.source, self.line) 
        self.tokens.append(t)
        self.index += 1


    def scan_equal_symbol(self) -> None:
        if self.peek() == '=':
            t: Token = Token(TokenType.EQUALITY_OP, self.index, 2, self.source, self.line) 
            self.tokens.append(t)
            self.index += 2
        else:
            t: Token = Token(TokenType.ASSIGNMENT, self.index, 1, self.source, self.line) 
            self.tokens.append(t)
            self.index += 1