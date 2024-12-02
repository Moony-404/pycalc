from typing import List
import sys

# Tokens for the scanner
class Token:
    def __init__(self, repr: str):
        self.repr: str = repr
        
    def __repr__(self) -> str:
        return self.repr

    def __str__(self) -> str:
        return self.repr

class NumericToken(Token):  
    def __init__(self, value: float):
        super().__init__(str(value))
        self.value: float = value

class IdentifierToken(Token):
    def __init__(self, s: str):
        super().__init__(str(s))
        self.word : str = s

class OperatorToken(Token):
    def __init__(self, op: str):
        super().__init__(op)
        self.op: str = op

class ParenToken(Token):
    def __init__(self, paren: str):
        super().__init__(paren)
        self.paren: str = paren

class EqualityToken(Token):
    def __init__(self):
        super().__init__("=")

class EOFToken(Token):
    def __init__(self):
        super().__init__('EOF')

class Scanner:
    numbers: str = '0123456789.'
    operators: str = '+-*/'
    parenthesis: str = '()'
    whitespaces: str = ' \t\n'

    def __init__(self):
        self.tokens: List[Token] = []
        self.string: str = ''
        self.index: int = 0

    def scan(self, text: str) -> None:
        self.string = text
        self.index = 0
        self.tokens = []

        while self.inside_string():
            if self.current_char in Scanner.numbers:
                self.scan_nums()
            elif self.current_char in Scanner.operators:
                self.scan_op()
            elif self.current_char in Scanner.whitespaces:
                self.index += 1
            elif self.current_char in Scanner.parenthesis:
                self.scan_paren()
            elif self.current_char == '=':
                self.scan_equality()
            elif self.current_char.isalpha():
                self.scan_identifier()
            else:
                print("Invalid syntax")
                self.tokens.clear()
                break

        # self.tokens.append(EOFToken())

    def inside_string(self) -> bool:
        return self.index < len(self.string)

    @property
    def current_char(self) -> str:
        return self.string[self.index]
    
    def scan_identifier(self) -> None:
        word: str = ''
        while self.inside_string() and (self.current_char.isalnum() or self.current_char == '_'):
            word += self.current_char
            self.index += 1

        self.tokens.append(IdentifierToken(word))

    def scan_nums(self) -> None:
        number: str = '' 
        decimal_count: int = 0
        while self.inside_string() and self.current_char in Scanner.numbers:
            if self.current_char == '.':
                decimal_count += 1
            number += self.current_char
            self.index += 1

        if decimal_count > 1:
            print(f"Syntax Error: {decimal_count} decimal points in a number")
            sys.exit()
        
        self.tokens.append(NumericToken(float(number)))

    def scan_op(self) -> None:
        self.tokens.append(OperatorToken(self.current_char))
        self.index += 1

    def scan_paren(self) -> None:
        self.tokens.append(ParenToken(self.current_char))
        self.index += 1

    def scan_equality(self) -> None:
        self.tokens.append(EqualityToken())
        self.index += 1
