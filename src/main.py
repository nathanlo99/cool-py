
from lexer import lex
from parser import *

source = open("examples/hello_world.cl", "r").read()

tokens = list(lex(source))

for token in tokens:
    print(token)
