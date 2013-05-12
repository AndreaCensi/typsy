from contracts import contract
from abc import abstractmethod 


class NotBelongs():
    @contract(space='space')
    def __init__(self, space, a):
        pass

class Space():
    # TODO: should be called Set

    @abstractmethod    
    def belongs(self, a):
        pass

    @abstractmethod    
    def equals(self, a, b):
        """
            raises: NotBelongs
        """
        pass


class EquivRelation():
    
    @contract(S=Space)
    def __init__(self, S):
        self._space = S

    @abstractmethod    
    @contract(a='in_space', b='in_space', returns='bool')
    def related(self, a, b):
        pass

