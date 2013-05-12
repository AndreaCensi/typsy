from contracts import contract
from genblocks.interfaces import Space

from sts import HasComponents


class StochasticProcess(Space, HasComponents):
    short = 'sp'
    
    @contract(o=Space)
    def __init__(self, o, t):
        self.o = o
        self.t = t
        
    def belongs(self, a):
        raise NotImplemented

    def equals(self, a, b):
        return a == b
    
    def to_struct(self):
        pass

    def __str__(self):
        return 'SP(%s;%s)' % (self.o, self.t)

