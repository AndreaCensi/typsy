from abc import abstractmethod
from contracts import contract
from typsy.library import Space



    
class EquivRelation():
    
    @contract(S=Space)
    def __init__(self, S):
        self._space = S

    @abstractmethod    
    @contract(a='in_space', b='in_space', returns='bool')
    def related(self, a, b):
        pass

