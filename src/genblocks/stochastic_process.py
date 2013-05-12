from contracts import contract
from genblocks.interfaces import Space, HasComponents


class StochasticProcess(Space, HasComponents):
    
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

    def get_components(self):
        return ['o', 't']
    
        
