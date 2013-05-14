from genblocks.interfaces import Space
from pyparsing import Literal, Suppress
from typsy import HasComponents
from typsy import simple_sts_type, sts_type

        
class OrbitSpace(Space, HasComponents):
    
    short = 'os'
    
    # @contract(s=Space, g=GroupAction)
    def __init__(self, s, g):
        self.space = s
        self.group = g 
    
    def belongs(self, a):
        return self.S.belongs(a)
        
    def equals(self, a, b):
        return self._group.related(a, b)
    
    def __repr__(self):
        return 'OrbitSpace(%r,%r)' % (self.space, self.group)
    
    def __str__(self):
        return '%s/%s' % (self.format_sub(self.space),
                          self.format_sub(self.group))

    @staticmethod
    def get_parsing_expr():
        S = Suppress
        inside = simple_sts_type | (S('(') - sts_type - S(')'))
        modulus = S(Literal('/'))
        expr = (inside + modulus - inside)
        
        def my_parse_action(s, loc, tokens):  # @UnusedVariable
            s = tokens[0]
            g = tokens[1]
            return OrbitSpace(s=s, g=g)
                
        expr.addParseAction(my_parse_action)
        expr.setName('orbit')
        return False, expr
    
    
    @staticmethod
    def get_parsing_examples():
        return """
        A/B
        
        
        """
        # ({0,1})/(Aut({0,1}))
