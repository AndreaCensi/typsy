from genblocks.interfaces import Mapping, Space
from genblocks import contract_inherit
from genblocks.product import Product
from genblocks.finite_set import FiniteSet
from contracts import contract


bit = FiniteSet([0, 1])

def bits(n):
    return Product(bit, n)                

class ConstantMapping(Mapping): 
    def __init__(self, i, o, value):
        Mapping.__init__(self, i=i, o=o)
        self.value = value
        
    @contract_inherit
    def __call__(self, v):  # @UnusedVariable
        return self.value 
    

class Interval(Space): 
    
    @contract(bounds='seq[2](number)')
    def __init__(self, bounds):
        self.lower = bounds[0]
        self.upper = bounds[1]
        
    def belongs(self, a):
        return self.lower <= a <= self.upper

    def equals(self, a, b):
        return a == b
    
    def to_struct(self):
        pass

    def __str__(self):
        return '[%s,%s] ' % (self.lower, self.upper)


