
from lexer import lex

source = open("examples/arith.cl", "r").read()

tokens = list(lex(source))

for token in tokens:
    print(token)
