
from collections import namedtuple

# class ClassDecl(namedtuple("ClassDecl", ("classname", "features"))):
#     def to_dict(self):
#         return {
#             "type": "ClassDecl",
#             "features": self.features.to_dict(),
#         }
#
# class FeatureList(namedtuple("FeatureList", "features")):
#     def to_dict(self):
#         return repr(self.features)

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

json.dumps(Expression(TokenStack(lex('4 * 5 + 3'))).node.to_dict(), sort_keys=True, indent=4, separators=(',', ': '))
