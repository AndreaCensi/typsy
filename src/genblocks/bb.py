from genblocks.interfaces import Space

from sts import HasComponents
from sts.has_comps import sts_type
from pyparsing import Literal, Suppress
from contracts import contract


class BlackBox(Space, HasComponents):
    short = 'bb'
    
    @contract(i=Space, o=Space)
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
