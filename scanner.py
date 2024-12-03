import sys
from typing import List, Optional
from _token import *


class Scanner:
    numbers: str = '0123456789.'
    operators: str = '+-*/%<>!'
    parenthesis: str = '()'
    braces: str = '{}'
    whitespaces: str = ' \t\n'

    def __init__(self):
        self.tokens: List[Token] = []
        self.string: str = ''
        self.index: int = 0


    def inside_string(self) -> bool:
        return self.index < len(self.string)

    @property
    def current_char(self) -> str:
        return self.string[self.index]
    
    def peek(self) -> Optional[str]:
        try:
            next_char: str = self.string[self.index + 1]
            return next_char
        except IndexError:
            return None
    
    def scan_brace(self) -> None:
        self.tokens.append(Brace(self.current_char))
        self.index += 1

    def scan_semicolon(self) -> None:
        self.tokens.append(Semicolon())
        self.index += 1

    def scan_identifier(self) -> None:
        '''
        Scans an identifier. Also checks if it is a keyword
        '''
        word: str = ''
        while self.inside_string() and (self.current_char.isalnum() or self.current_char == '_'):
            word += self.current_char
            self.index += 1

        if word == 'and' or word == 'or':
            self.tokens.append(LogicalOP(word))
        elif word == 'not':
            self.tokens.append(NotOP())
        elif word == 'True':
            self.tokens.append(Boolean(True))
        elif word == 'False':
            self.tokens.append(Boolean(False))
        else:
            self.tokens.append(Identifier(word))
        return

    def scan_number(self) -> None:
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
        
        self.tokens.append(NumberToken(float(number)))

    def scan_string(self) -> None:
        s : str = ''
        self.index += 1
        while self.inside_string() and self.current_char != '"':
            s += self.current_char
            self.index += 1

        try:
            if self.current_char == '"':
                self.tokens.append(String(s))
                self.index += 1
        except IndexError:
            raise SyntaxError("Expected a \" at the end of string")
        return

    def scan_operator(self) -> None:
        math_operator = '+-*/%'
        relational_operator = '<>'

        if self.current_char in math_operator:
            self.tokens.append(MathOP(self.current_char))
            self.index += 1

        elif self.current_char in relational_operator:
            if self.peek() == '=':
                self.tokens.append(RelationalOP(self.current_char + '='))
                self.index += 2
            else:
                self.tokens.append(RelationalOP(self.current_char))
                self.index += 1

        else:
            if self.peek() == '=':
                self.tokens.append(RelationalOP('!='))
                self.index += 2
            else:
                raise SyntaxError("'!' is not an operator. Did you mean 'not'?")
        return

    def scan_parenthesis(self) -> None:
        self.tokens.append(Parenthesis(self.current_char))
        self.index += 1

    def scan_equal_symbol(self) -> None:
        if self.peek() == '=':
            self.tokens.append(RelationalOP('=='))
            self.index += 2
        else:
            self.tokens.append(AssignmentOP())
            self.index += 1
    
    def scan(self, text: str) -> None:
        # Initialize the state of the scanner
        self.string = text
        self.index = 0
        self.tokens.clear()

        while self.inside_string():
            if self.current_char in Scanner.numbers:
                self.scan_number()  # done 
            elif self.current_char == '"':
                self.scan_string() # done
            elif self.current_char.isalpha():
                self.scan_identifier() # done
            elif self.current_char in Scanner.operators:
                self.scan_operator() # done
            elif self.current_char in Scanner.parenthesis:
                self.scan_parenthesis() # done
            elif self.current_char == '=':
                self.scan_equal_symbol() # done
            elif self.current_char in Scanner.whitespaces:
                self.index += 1 # done
            elif self.current_char in Scanner.braces:
                self.scan_brace() #done
            elif self.current_char == ';':
                self.scan_semicolon()
            else:
                print("Invalid syntax")
                # For debugging purposes, we are not clearing the token list
                # self.tokens.clear()
                break

        self.tokens.append(EOFToken())