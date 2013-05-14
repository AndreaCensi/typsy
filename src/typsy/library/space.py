from typsy.has_comps import HasComponents
from pyparsing import Literal, Suppress
from abc import abstractmethod
from contracts import contract

class Space(HasComponents):
    short = 'space'

    def __init__(self):
        pass
    
    @staticmethod
    def get_parsing_examples():
        return ""
 
    def __repr__(self):
        return 'Space()'
    
    def __str__(self):
        return 'Space'
    
    @staticmethod
    def get_parsing_expr():
        S = Suppress
        L = Literal
        expr = (S(L('Space')))
        expr.setName('bb')
        
        def parse_action(s, loc, tokens):  # @UnusedVariable
            # print('tokens: %r' % tokens)
            return Space()
        
        expr.setParseAction(parse_action)
        return True, expr


class NotBelongs():
    @contract(space=Space)
    def __init__(self, space, a):
        pass
    
class ConcreteSpace(Space):
    
    @abstractmethod     
    def belongs(self, a):
        pass
    
    @abstractmethod
    def equals(self, a, b):
        pass


