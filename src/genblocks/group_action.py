from genblocks.interfaces import EquivRelation, Space
from contracts import contract
from abc import ABCMeta, abstractmethod


class GroupAction(EquivRelation):
    
    __metaclass__ = ABCMeta
    
    @contract(S=Space)
    def __init__(self, S):
        self._space = S
        
    @abstractmethod
    @contract(returns='bool')
    def related(self, a, b):
        """ Yes if  a = g.b """
        raise NotImplemented


class GProduct(GroupAction):
    def __init__(self, s, n):
        self.s = s
        self.n = n
        
    @contract(returns='bool')
    def related(self, a, b):
        raise NotImplemented
        
    def __str__(self):
        return '(%s)^%s' % (self.s, self.n)


class Automorphism(GroupAction):
    @contract(s=Space)
    def __init__(self, s):
        self.s = s
        
    def __str__(self):
        return 'Aut(%s)' % self.s

    def related(self, a, b):
        return True
    
