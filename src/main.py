
from lexer import lex
from parser import *

import json


def prettify(dict_):
    print(json.dumps(dict_, sort_keys=True, indent=4, separators=(',', ': ')))

parse_output = ClassDeclExpression(TokenStack(
    lex(open("examples/hello_world.cl", "r").read()))).node

# prettify(parse_output.to_dict())

print(parse_output.to_readable())
