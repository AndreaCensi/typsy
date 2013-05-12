from genblocks.interfaces import EquivRelation, Space
from contracts import contract
from abc import abstractmethod
from sts.has_comps import HasComponents

class GroupAction(HasComponents, EquivRelation):
    short = 'action'
    
    @contract(S=Space)
    def __init__(self, S):
        self.S = S
        
    @abstractmethod
    @contract(returns='bool')
    def related(self, a, b):
        """ Yes if  a = g.b """
        raise NotImplemented

    @staticmethod
    def get_parsing_expr():
        return None


class GProduct(GroupAction):
    short = 'gprod'
    
    def __init__(self, s, n):
        self.s = s
        self.n = n
        
    @contract(returns='bool')
    def related(self, a, b):
        raise NotImplemented
        
    def __str__(self):
        return '(%s)^%s' % (self.s, self.n)

    @staticmethod
    def get_parsing_expr():
        return None

class Automorphism(GroupAction):
    short = 'aut'
    
    @contract(s=Space)
    def __init__(self, s):
        self.s = s
        
    def __str__(self):
        return 'Aut(%s)' % self.s

    def related(self, a, b):
        return True
    
