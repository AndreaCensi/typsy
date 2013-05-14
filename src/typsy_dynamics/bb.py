from typsy import Space, Numeric, sts_type
from pyparsing import Literal, Suppress
 

class BlackBox(Space):
    short = 'bb'
    
    # @contract(i=Space, o=Space)
    def __init__(self, o, i, t):
        self.i = i
        self.o = o
        self.t = t
        
    def belongs(self, a):
        raise NotImplemented
        
    def equals(self, a, b):
        raise NotImplemented

    def __str__(self):
        return 'BB(%s;%s;%s)' % (self.o, self.i, self.t)

    def __repr__(self):
        return 'BlackBox(%r,%r,%r)' % (self.o, self.i, self.t)
    
    def match_components(self, variables, spec):
        Space.match_components(self, variables, spec)
        self.i.match(variables, Space())
        self.o.match(variables, Space())
        self.t.match(variables, Numeric())
    
    @staticmethod
    def get_parsing_expr():
        L = Literal
        S = Suppress
        expr = (S(L('BB')) - S(L('(')) - sts_type - S(L(';')) - sts_type - S(L(';')) 
                - sts_type - S(L(')')))
        
        expr.setName('bb')
        
        def parse_action(s, loc, tokens):  # @UnusedVariable
            # print('tokens: %r' % tokens)
            o = tokens[0]
            i = tokens[1]
            t = tokens[2]
            return BlackBox(i=i, o=o, t=t)
        
        expr.setParseAction(parse_action)
        return True, expr

    @staticmethod
    def get_parsing_examples():
        return """
        BB({0};{1};$t)
        BB({0};{1,2};$t)
        """
