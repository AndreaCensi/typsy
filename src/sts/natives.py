from sts.has_comps import HasComponents
from sts.exceptions import FailedMatch

class PGNative(HasComponents):
    short = 'native'
    
    def __init__(self, value):
        self.value = value
        
    def get_components(self):
        return []
    
    def match(self, variables, other):  # @UnusedVariable
        if not(self.value == other.value):
            raise FailedMatch(self, other)
    
    def replace_vars(self, variables):  # @UnusedVariable
        return self
    
    def __repr__(self):
        return 'PGNative(%r)' % self.value
    
    def __str__(self):
        return self.value.__repr__()
        
class PGList(list, HasComponents):
    short = 'list'
    
    def match(self, variables, other):
        for s1, s2 in zip(self, other):
            HasComponents.debug_level += 1
            s1.match(variables, s2)
            HasComponents.debug_level -= 1
    
    def replace_vars(self, variables):
        l = [c.replace_vars(variables) for c in self]
        return PGList(l)


def as_gb(value):
    if isinstance(value, list):
        return PGList(map(as_gb, value))
    else:
        return PGNative(value)

