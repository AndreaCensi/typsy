from contracts import contract
from abc import abstractmethod
from sts import HasComponents


class NotBelongs():
    @contract(space='space')
    def __init__(self, space, a):
        pass

class Space():
    # TODO: should be called Set
#     __metaclass__ = ABCMeta
        
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


class Mapping(HasComponents): 
    short = 'map'
    
    # @contract(i=Space, o=Space)
    # TODO: generic
    def __init__(self, i, o):
        self.i = i
        self.o = o

    @contract(v='in_input', returns='in_output')
    def __call__(self, v):
        pass
    
    def to_struct(self):
        return {'i': self.i, 'o': self.o}
    
    def __str__(self):
        return "(%s)->(%s)" % (self.i, self.o)

