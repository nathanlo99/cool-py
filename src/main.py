
from lexer import lex
from parser import *

import json

def prettify(dict_):
    print(json.dumps(dict_, sort_keys=True, indent=4, separators=(',', ': ')))

prettify(ClassDeclExpression(TokenStack(lex(open("examples/hello_world.cl", "r").read()))).node.to_dict())
