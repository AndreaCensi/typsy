from sts.has_comps import sts_type, HasComponents, simple_sts_type
from pyparsing import Literal, Suppress
from contracts import contract


class Mapping(HasComponents): 
    short = 'map'
    
    # @contract(i=Space, o=Space)
    # TODO: generic
    def __init__(self, i, o):
        self.i = i
        self.o = o

    @contract(v='in_input', returns='in_output')
    def __call__(self, v):
        pass
    
    def to_struct(self):
        return {'i': self.i, 'o': self.o}
    
    def __repr__(self):
        return 'Mapping(%r, %r)' % (self.i, self.o)
    
    def __str__(self):
        return "(%s)->(%s)" % (self.i, self.o)

    @staticmethod
    def get_parsing_expr():
        S = Suppress
        inside = (S('(') - sts_type - S(')')) | simple_sts_type
        expr = (inside + S(Literal('->')) - inside)
        
        def my_parse_action(s, loc, tokens):  # @UnusedVariable
            i = tokens[0]
            o = tokens[1]
            return Mapping(i, o)
                
        expr.addParseAction(my_parse_action)
        
        return False, expr
    
    @staticmethod
    def get_parsing_examples():
        return """
        ({0}) -> ({1})
        ({0})->(({0})->({1}))

        """
