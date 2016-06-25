
# The lexer tokenizes the source code into lexemes, or tokens
import re
from collections import namedtuple

class TokenDef(namedtuple("TokenType", ("name", "pattern", "type_filter"))):
    def __repr__(self):
        return "TokenType." + self.name

class TokenType(object):
    _ignore = [
        "multi_line",
        "single_line",
        "whitespace",
        "new_line",
    ]
    _keywords = [
        "class", "inherits", "case", "self", "of", "new", "esac", "let", "in",
        "if", "then", "else", "fi", "loop", "pool", "while", "not"
    ]
    _literals = {
        "+": "plus",
        "-": "minus",
        "*": "times",
        "/": "divide",
        "(": "left_paren",
        ")": "right_paren",
        "{": "left_brace",
        "}": "right_brace",
        ",": "comma",
        "~": "tilda",
        ":": "colon",
        ";" : "semicolon",
        "." : "dot",
        "@" : "at",
        "<-" : "left_arrow",
        "=>" : "right_arrow",
        "<" : "less_than",
        "=" : "equals",
    }
    _defs = [
        TokenDef("multi_line", re.compile("\(\*(.|[\r\n])*?\*\)"), None),
        TokenDef("single_line", re.compile("--[^\n]*"), None),
        TokenDef("string_literal", re.compile("\"(\\.|[^\n\"])*\""), None),
        TokenDef("identifier", re.compile("[A-Za-z_][A-Za-z_0-9]*"), None),
        TokenDef("whitespace", re.compile("[\t ]+"), None),
        TokenDef("new_line", "\n", None),
        TokenDef("integer_literal", re.compile("[0-9]+"), int)
    ]

for pattern, name in TokenType._literals.items():
    TokenType._defs.append(TokenDef(name, pattern, None))

for def_ in TokenType._defs:
    setattr(TokenType, def_.name, def_)

for keyword in TokenType._keywords:
    setattr(TokenType, "keyword_" + keyword, TokenDef("keyword_" + keyword, keyword, None))

class Token(namedtuple("Token", ("type", "raw_value", "value", "slice"))):
    def __repr__(self):
        return "Token." + self.type.name + "(" + repr(self.value) + ")"

def next_token(source, start=0):
    match_text = source[start:]
    token = None
    token_text = None
    for type_ in TokenType._defs:
        name, pattern, value_filter = type_
        if pattern is None:
            continue
        elif isinstance(pattern, str):
            if not match_text.startswith(pattern):
                continue
            match_value = pattern
        else:
            match = pattern.match(match_text)
            if not match:
                continue
            match_value = match.group(0)

        if token_text is None or len(match_value) > len(token_text):
            token_text = match_value
            if value_filter is not None:
                match_value = value_filter(match_value)
            if type_ is TokenType.identifier and match_value in TokenType._keywords:
                type_ = getattr(TokenType, "keyword_" + match_value)
            token = Token(type_, token_text, match_value, slice(start, start + len(token_text)))

    return token

def lex(source):
    print("Lexing... ")
    line_no = 1
    char_no = 1
    start = 0
    length = len(source)
    while True:
        if start >= length:
            break
        token = next_token(source, start)
        if token is None:
            backtrace_start = max(0, start - 10, start - char_no + 1)
            source_line = source[backtrace_start:].splitlines()[0]
            error_pointer = start - backtrace_start
            print("Lexing failed at Line " + str(line_no) + " : Col " + str(char_no))
            print(source_line)
            print(" " * error_pointer + "^")
        if token.type.name not in TokenType._ignore:
            yield token
        start = token.slice.stop

        if token.type is TokenType.new_line:
            line_no += 1
            char_no = 1
        elif token.type is TokenType.multi_line:
            line_no += token.raw_value.count("\n")
            char_no = len(token.raw_value.splitlines()[-1])
        else:
            char_no += len(token.raw_value)
