
from collections import namedtuple


class AssignmentNode(namedtuple("AssignmentNode", ("id", "value"))):

    def to_dict(self):
        return {
            "type": "AssignmentNode",
            "id": self.id,
            "value": self.value.to_dict() if type(self.value) is not str else "void",
        }

    def to_readable(self):
        return "{} = {};".format(self.id, self.value.to_readable())


class SelfDispatchNode(namedtuple("SelfDispatchNode", ("caller", "method_name", "arguments"))):

    def to_dict(self):
        return {
            "type": "SelfDispatchNode",
            "caller": self.caller,
            "method_name": self.method_name,
            "arguments": self.arguments,
        }

    def to_readable(self):
        return "({}).{}({});".format(self.caller, self.method_name, self.arguments)


class UnqualifiedDispatchExpression(namedtuple("UnqualifiedDispatch", ("method_name", "arguments"))):

    def to_dict(self):
        return {
            "type": "UnqualifiedDispatch",
            "name": self.method_name,
            "arguments": self.arguments,
        }


class MethodDeclNode(namedtuple("MethodDecl", ("name", "parameters", "return_type", "statement"))):

    def to_dict(self):
        return {
            "type": "MethodDecl",
            "name": self.name,
            "parameters": self.parameters,
            "return_type": self.return_type,
            "statement": self.statement.to_dict()
        }

    def to_readable(self):
        return "{} {} ({}) {{ \n{}\n}}".format(self.return_type, self.name, ", ".join(str(x) for x in self.parameters), self.statement.to_readable())


class ClassDeclNode(namedtuple("ClassDecl", ("classname", "super", "features"))):

    def to_dict(self):
        return {
            "type": "ClassDecl",
            "super": self.super,
            "name": self.classname,
            "features": [feature.to_dict() for feature in self.features],
        }

    def to_readable(self):
        return "class {} extends {} {{ \n{}\n}};".format(self.classname, self.super, "\n\t".join(feature.to_readable() for feature in self.features))


class AttributeDeclNode(namedtuple("AttributeDeclNode", ("name", "type", "value"))):

    def to_dict(self):
        return {
            "type": "AttributeDeclNode",
            "name": self.name,
            "attr_type": self.type,
            "value": self.value.to_dict() if self.value is not "void" else "void",
        }

    def to_readable(self):
        return "{} {} = {};".format(self.type, self.name, self.value.to_readable() if self.value is not "void" else "void")


class VariableReference(namedtuple("VariableReference", "value")):

    def to_dict(self):
        return {
            "type": "VariableReference",
            "value": self.value,
        }

    def to_readable(self):
        return "${}".format(self.value)


class BinaryOpNode(namedtuple("BinaryOpNode", ("lhs", "op", "rhs"))):

    def to_dict(self):
        return {
            "type": "BinaryOpNode",
            "lhs": self.lhs.to_dict(),
            "op": self.op,
            "rhs": self.rhs.to_dict()
        }

    def to_readable(self):
        return "({}) {} ({})".format(self.lhs.to_readable(), self.op, self.rhs.to_readable())


class UnaryOpNode(namedtuple("UnaryOpNode", ("op", "rhs"))):

    def to_dict(self):
        return {
            "type": "UnaryOpNode",
            "op": self.op,
            "rhs": self.rhs.to_dict()
        }

    def to_readable(self):
        return "{}({})".format(self.op, self.rhs.to_readable())


class IntegerNode(namedtuple("IntegerNode", "value")):

    def to_dict(self):
        return {
            "type": "IntegerNode",
            "value": self.value,
        }

    def to_readable(self):
        return str(self.value)


class StringNode(namedtuple("StringNode", "value")):

    def to_dict(self):
        return {
            "type": "StringNode",
            "value": self.value,
        }

    def to_readable(self):
        return self.value
