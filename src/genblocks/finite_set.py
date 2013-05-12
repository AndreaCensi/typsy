from genblocks.interfaces import Space, HasComponents, FailedMatch
from contracts import contract

class FiniteSet(Space, HasComponents):
    
    @contract(values='list')
    def __init__(self, values):
        self._values = values
        
    def belongs(self, a):
        return a in self._values

    def equals(self, a, b):
        return a == b
    
    def get_values(self):
        return list(self._values)
    
    def to_struct(self):
        pass

    def __str__(self):
        elems = ",".join('%s' % x for x in self._values)
        return '{' + elems + '}'
 
    def get_components(self):
        return []     
          
    def match(self, variables, other):  
        if not isinstance(other, FiniteSet):
            raise FailedMatch(self, other)
        if not self.get_values() == other.get_values():
            raise FailedMatch(self, other)
    
    
