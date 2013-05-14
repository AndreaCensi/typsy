from typsy.has_comps import HasComponents, sts_type
from typsy.library.space import Space
from contracts import contract
from pyparsing import Literal

class Interval(HasComponents, Space): 
    short = 'interval'
    
    @contract(bounds='seq[2]')
    def __init__(self, bounds):
        self.lower = bounds[0]
        self.upper = bounds[1]
        
    def belongs(self, a):
        return self.lower <= a <= self.upper

    def equals(self, a, b):
        return a == b
    
    def to_struct(self):
        pass

    def __str__(self):
        return '[%s,%s] ' % (self.lower, self.upper)

    @staticmethod
    def get_parsing_expr():
        expr = Literal('[') + sts_type + "," + sts_type + Literal(']')    
        expr.setName('Interval')
        return True, expr
    
