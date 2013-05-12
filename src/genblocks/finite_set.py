from contracts import contract
from genblocks.interfaces import Space 

from sts import HasComponents, as_gb
    
class FiniteSet(Space, HasComponents):
    short = 'set'
    
    @contract(values='list')
    def __init__(self, values):
        self.values = as_gb(values)
        
    def belongs(self, a):
        return a in self.values

    def equals(self, a, b):
        return a == b
    
    def get_values(self):
        return list(self._values)
    
    def to_struct(self):
        pass

    def __str__(self):
        elems = ",".join('%s' % x for x in self.values)
        return '{' + elems + '}'
 
    def __repr__(self):
        return 'FiniteSet(%r)' % self.values
    
    
