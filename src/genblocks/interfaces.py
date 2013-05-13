from contracts import contract
from abc import abstractmethod 
from sts.has_comps import HasComponents
from pyparsing import Literal, Suppress


class NotBelongs():
    @contract(space='space')
    def __init__(self, space, a):
        pass



class SpaceType(HasComponents):
    short = 'space'
    # TODO: should be called Set

    def __init__(self):
        pass
    
    # @abstractmethod    
    # def belongs(self, a):
    #    pass
    @staticmethod
    def get_parsing_examples():
        return ""
 
    def __repr__(self):
        return 'SpaceType()'
    
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
            return SpaceType()
        
        expr.setParseAction(parse_action)
        return True, expr

Space = SpaceType
#     @abstractmethod    
#     def equals(self, a, b):
#         """
#             raises: NotBelongs
#         """
#         pass


class Numeric(Space):
    short = 'numeric'

    def __init__(self):
        pass

    @staticmethod
    def get_parsing_examples():
        return "Numeric"
 
    def __repr__(self):
        return 'Numeric()'
    
    def __str__(self):
        return 'Numeric'
    
    @staticmethod
    def get_parsing_expr():
        S = Suppress
        L = Literal
        expr = (S(L('Numeric')))
        expr.setName('Numeric')
        
        def parse_action(s, loc, tokens):  # @UnusedVariable
            return Numeric()
        
        expr.setParseAction(parse_action)
        return True, expr
    
    
    
class EquivRelation():
    
    @contract(S=Space)
    def __init__(self, S):
        self._space = S

    @abstractmethod    
    @contract(a='in_space', b='in_space', returns='bool')
    def related(self, a, b):
        pass

