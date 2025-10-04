#!/usr/bin/python3
import sys
from interpreter import *

i = Interpreter()

argc = len(sys.argv)
if argc == 1:
    i.repl()

elif argc == 2:
    file = sys.argv[1]
    with open(file, 'r') as f:
        source = f.read()
        i.run(source)

else:
    print(f"usage: {sys.argv[0]} [file]\n")