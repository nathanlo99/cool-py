
from collections import namedtuple

class AssignmentNode(namedtuple("AssignmentNode", ("id", "value"))):
    def to_dict(self):
        return {
            "type": "AssignmentNode",
            "id": self.id,
            "value": self.value,
        }

class SelfDispatchNode(namedtuple("SelfDispatchNode", ("caller", "method_name", "arguments"))):
    def to_dict(self):
        return {
            "type": "SelfDispatchNode",
            "caller": self.caller,
            "method_name": self.method_name,
            "arguments": self.arguments,
        }

class ClassDeclNode(namedtuple("ClassDecl", ("classname", "super", "features"))):
    def to_dict(self):
        return {
            "type": "ClassDecl",
            "super": self.super,
            "features": [feature.to_dict() for feature in self.features],
        }

class AttributeDeclNode(namedtuple("AttributeDeclNode", ("name", "type", "value"))):
    def to_dict(self):
        return {
            "type": "AttributeDeclNode",
            "name": self.name,
            "attr_type": self.type,
            "value": self.value.to_dict() if self.value is not "void" else "void",
        }

class BinaryOpNode(namedtuple("BinaryOpNode", ("lhs", "op", "rhs"))):
    def to_dict(self):
        return {
            "type" : "BinaryOpNode",
            "lhs" : self.lhs.to_dict(),
            "op" : self.op,
            "rhs" : self.rhs.to_dict()
        }

class UnaryOpNode(namedtuple("UnaryOpNode", ("op", "rhs"))):
    def to_dict(self):
        return {
            "type" : "UnaryOpNode",
            "op": self.op,
            "rhs": self.rhs.to_dict()
        }

class IntegerNode(namedtuple("IntegerNode", "value")):
    def to_dict(self):
        return {
            "type": "IntegerNode",
            "value": self.value
        }

class StringNode(namedtuple("StringNode", "value")):
    def to_dict(self):
        return {
            "type": "StringNode",
            "value": self.value,
        }
