from typsy import Numeric
from typsy.parseables import  ParseableWithExpression
 
class BlackBox(ParseableWithExpression):
 
    @classmethod
    def get_identifier(cls):
        return 'BB'
    
    def __init__(self, o, i, t):
        self.i = i
        self.o = o
        self.t = t
        
    def __repr__(self):
        return 'BlackBox(%r,%r,%r)' % (self.o, self.i, self.t)

    
    def belongs(self, a):
        raise NotImplemented
        
    def equals(self, a, b):
        raise NotImplemented

    
    def match_components(self, variables, spec):
        ParseableWithExpression.match_components(self, variables, spec)
#         self.i.match(variables, Space2())
#         self.o.match(variables, Space2())
        self.t.match(variables, Numeric())
     

    @staticmethod
    def get_parsing_examples():
        return """
        BB({0};{1};$t)
        BB({0};{1,2};$t)
        """
