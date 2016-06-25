
from lexer import lex
from parser import *

import json

print(json.dumps(ClassDeclExpression(TokenStack(lex(open("examples/hello_world.cl", "r").read()))).node.to_dict(), sort_keys=True, indent=4, separators=(',', ': ')))
