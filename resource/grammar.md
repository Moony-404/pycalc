## How does the interpreter handle errors in the code?

An error can occur in multiple parts of the interpreter, in the scanner, or the parser or the execution itself.

If the error occur in the scanner then it is a lexical error. The user may have entered a symbol that the scanner doesn't understand
For all these symbols the scanner will emit a `UnknownSymbol` exception. This exception is caught by the wrapper class, Interpreter, and
handled accordingly.

The goal should be to emit as many errors as possible in a single pass. In order to achieve that the interpreter treats different
statements separately. It looks for error in each statement and print it to the standard output. If an error was found in the
scanning phase then the subsequent phases of compilation aren't run.

## Grammar for the language

```text
program : declaration\* EOF;

declaration : letStatement | statement;

statement : printStmt | expressionStmt;
```

Here we make a distinction between statements and expressions. An expression is something that can be evaluated while a statement
changes some internal state of the interpreter or produces some side-effects. Having distinct classes for statements and expressions
allows the parser to notice silly mistakes like passing a statement to `print` or assigning a statement to a variable.

So read the following lines as `expressionStmt` contains an assignment expression instead of being an expression. An expression is
composed inside the `expressionStmt` instead of being used in place of a one.

```
letStatement : let IDENTIFIER '=' assignment ';';
printStmt : 'print' assignment ';'
```

```text
expressionStmt : assignment;

assignment : logicalExpr ('=' assignment)? ';' | logicalExpr ';' ;
```

The `lvalue` of an assignment expression can only be a subset of all possible expression. Right now, it can only be an identifier which
is already in the interpreter's environment. The rest of the grammar is given below.

```text
logicalExpr : equalityExpr ('and' | 'or') logicalExpr | equalityExpr;

equalityExpr : relationalExpr ('=='|'!=') equalityExpr | relationalExpr;

relationalExpr : addExpr ('<'|'<='|'>='|'>') relationalExpr | addExpr;

addExpr : modExpr ('+'|'-') addExpr | modExpr;

modExpr : mulExpr '%' modExpr | mulExpr;

mulExpr : unaryExpr ('*'|'/') mulExpr | unaryExpr;

unaryExpr : '-' unaryExpr | 'not' unaryExpr | primary;

primary : NUMBER | IDENTIFIER | BOOLEAN | '('logical Expr')';
```

What are all the tokens needed for this simple language

1. `Number`
2. `String`
3. `Identifier`
4. `Boolean`
5. `Parenthesis`
6. `Brace`
7. `MathOP`
8. `RelationalOP`
9. `EqualityOP`
10. `LogicalOP`
11. `AssignmentOP`
12. `NotOP`
13. `Semicolon`
14. `EOFToken`
