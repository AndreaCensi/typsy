from pyparsing import Literal, Suppress
from typsy.has_comps import sts_type
from typsy import Space


class StochasticProcess(Space):
    short = 'sp'
    
    # @contract(o=Space)
    def __init__(self, o, t):
        self.o = o
        self.t = t
        
    def belongs(self, a):
        raise NotImplemented

    def equals(self, a, b):
        return a == b
 
    @staticmethod
    def get_parsing_expr():
        L = Literal
        S = Suppress
        expr = (S(L('SP')) + S(L('(')) + sts_type + S(L(';')) + sts_type + S(L(')')))
        
        def parse_action(s, loc, tokens):  # @UnusedVariable
            o = tokens[0]
            t = tokens[1]
            return StochasticProcess(o, t)
        
        expr.setParseAction(parse_action)
        expr.setName('SP')
        return True, expr


    @staticmethod
    def get_parsing_examples():
        return """
        SP({1};$t)
        SP({1,2};$t)
        """
        
    def __str__(self):
        return 'SP(%s;%s)' % (self.o, self.t)

    def __repr__(self):
        return 'StochasticProcess(%r,%r)' % (self.o, self.t)
