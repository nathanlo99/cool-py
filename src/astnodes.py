
from collections import namedtuple

class ClassDeclNode(namedtuple("ClassDecl", ("classname", "super", "features"))):
    def to_dict(self):
        return {
            "type": "ClassDecl",
            "super": self.super,
            "features": self.features,
        }

class AttributeDeclNode(namedtuple("AttributeDeclNode", ("name", "type", "value"))):
    def to_dict(self):
        return {
            "type": "AttributeDeclNode",
            "name": self.name,
            "type": self.type,
            "value": self.value,
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
