
from lexer import *
from astnodes import *

class ParseError(Exception):
    def __init__(self, message, *tokens):
        self.message = message
        self.tokens = tokens

    def __str__(self):
        if len(self.tokens) == 0:
            return self.message
        return "{0}-{1}:\n{2}".format(self.tokens[0].slice.start, self.tokens[-1].slice.stop - 1, self.message)

class TokenStack(object):
    def __init__(self, tokens):
        self._tokens = list(tokens)
        self._cursor = 0
        self._cursor_stack = []

    def __str__(self):
        return str(self._tokens[self._cursor:])

    def peek(self):
        try:
            return self._tokens[self._cursor]
        except IndexError:
            raise ParseError("Unexpected end of input")

    def pop(self):
        result = self.peek()
        self._cursor += 1
        return result

    def push_cursor(self):
        self._cursor_stack.append(self._cursor)

    def pop_cursor(self):
        self._cursor = self._cursor_stack.pop()

class ParserBase(object):
    def __init__(self, token_stack):
        self.token_stack = token_stack
        self.node = self.parse()

    def parse(self):
        raise NotImplementedError()

    def pop_expecting(self, types):
        result = self.token_stack.pop()
        if result.type not in types:
            raise ParseError("Unexpected token: \nExpected: {0} \nGot: {1}".format(str(types), result.type), result)
        return result

class IntegerLiteralExpression(ParserBase):
    def parse(self):
        int_token = self.pop_expecting([TokenType.integer_literal])
        return IntegerNode(int_token.value)

class UnaryOpExpression(ParserBase):
    def parse(self):
        op_token = self.pop_expecting([TokenType.tilda, TokenType.keyword_not])
        rhs_node = Expression(self.token_stack).node
        return UnaryOpNode(op_token.value, rhs_node)

class BracketedExpression(ParserBase):
    def parse(self):
        self.pop_expecting([TokenType.left_paren])
        expr_node = Expression(self.token_stack).node
        self.pop_expecting([TokenType.right_paren])
        return expr_node

class PrimaryExpression(ParserBase):
    expressions = [IntegerLiteralExpression, UnaryOpExpression, BracketedExpression]
    def try_to_parse(self, parser):
        for expression_type in self.expressions:
            try:
                self.token_stack.push_cursor()
                return parser(self.token_stack).node, True
            except ParseError:
                self.token_stack.pop_cursor()
                return None, False

    def parse(self):
        for parser in self.expressions:
            rv, ok = self.try_to_parse(parser)
            if ok: return rv
        raise ParseError("Expected integer, unary op or bracketed expression, but found none of those")

class BinaryExpression(ParserBase):
    _op_precedence = {
        '+': 1, '-': 1, '*': 2, '/': 2, '^': 3
    }

    def parse(self):
        return self.parse_expression(PrimaryExpression(self.token_stack).node)

    def parse_expression(self, lhs, min_precedence = 0):
        while self.next_is_binary() and self.precedence() >= min_precedence:
            op_token = self.token_stack.pop()
            rhs = PrimaryExpression(self.token_stack).node
            while self.next_is_binary() and self.precedence() > self.precedence(op_token):
                rhs = self.parse_expression(rhs, self.precedence())
            lhs = BinaryOpNode(lhs, op_token.value, rhs)
        return lhs

    def next_is_binary(self):
        try: next_token = self.token_stack.peek()
        except ParseError: return False
        return next_token.value in BinaryExpression._op_precedence

    def precedence(self, token = None):
        token = token or self.token_stack.peek()
        return BinaryExpression._op_precedence[token.value]

Expression = BinaryExpression

class AttributeDeclExpression(ParserBase):
    def parse(self):
        # <id> : <type> [ <- <expr> ];
        attribute_name = self.pop_expecting([TokenType.identifier]).value
        self.pop_expecting([TokenType.colon])
        attribute_type = self.pop_expecting([TokenType.identifier]).value
        try:
            self.token_stack.push_cursor()
            self.pop_expecting([TokenType.left_arrow])
            value = Expression(self.token_stack).node
        except ParseError:
            self.token_stack.pop_cursor()
            value = "void"
        self.pop_expecting([TokenType.semicolon])
        return AttributeDeclNode(attribute_name, attribute_type, value)

class MethodDeclExpression(ParserBase):
    def parse(self):
        # <id>(<id> : <type>[,])* : { <expr> };
        pass


class ClassDeclExpression(ParserBase):
    def parse(self):
        self.pop_expecting([TokenType.keyword_class])
        class_name = self.pop_expecting([TokenType.identifier]).value
        if self.token_stack.peek().type is TokenType.keyword_inherits:
            self.token_stack.pop()
            super_class = self.pop_expecting([TokenType.identifier]).value
        else:
            super_class = "Object"
        print("===== SUPER CLASS IS {} =====".format(super_class))
        self.pop_expecting([TokenType.left_brace])
        features = []
        while True:
            print(features)
            try:
                print("===== TRYING TO PARSE ATTRIBUTE =====")
                self.token_stack.push_cursor()
                features.append(AttributeDeclExpression(self.token_stack).node)
                print(features)
            except ParseError:
                self.token_stack.pop_cursor()
                break
            try:
                self.token_stack.push_cursor()
                features.append(MethodDeclExpression(self.token_stack).node)
            except ParseError:
                self.token_stack.pop_cursor()
                break
        self.pop_expecting([TokenType.right_brace])
        self.pop_expecting([TokenType.semicolon])
        return ClassDeclNode(class_name, super_class, features)
