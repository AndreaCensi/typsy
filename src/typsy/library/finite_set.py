from contracts import contract
from genblocks.interfaces import Space 

from typsy import HasComponents
from pyparsing import Suppress, Group, ZeroOrMore, Literal
from typsy.has_comps import sts_type, Parseable, ParseableWithOperators
from typsy.special import as_gb
    
__all__ = ['FiniteSet']

class FiniteSet(Space, Parseable):
    
    @contract(values='list')
    def __init__(self, values):
        self.values = as_gb(values)
        
    def belongs(self, a):
        return a in self.values

    def equals(self, a, b):
        return a == b
    
    def get_values(self):
        return list(self._values)
    
    def to_struct(self):
        pass

    def __str__(self):
        elems = ",".join('%s' % x for x in self.values)
        return '{' + elems + '}'
 
    def __repr__(self):
        return 'FiniteSet(%r)' % self.values

    @staticmethod
    def get_parsing_expr():
        S = Suppress    
        inside = (S('(') - sts_type - S(')')) | sts_type
        elements = S(Literal('{')) + inside + ZeroOrMore(S(',') + inside) \
                     + S(Literal('}'))
        elements = Group(elements)('elements')
        expr = elements
        expr.setName('Finite set')
        
        def parse_action(s, loc, tokens):  # @UnusedVariable
            values = list(tokens[0])
            return FiniteSet(values)
        
        expr.setParseAction(parse_action)
        
        return True, expr 

    @classmethod
    def get_precedence(klass):  # @UnusedVariable
        return 0

    @staticmethod
    def get_parsing_examples():
        return """
        {0,0}
        {1}

        """
