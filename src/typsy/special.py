from typsy.has_comps import HasComponents
from typsy.natives import PGNative

    
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

    @staticmethod
    def get_parsing_expr():
        return None
    
    @staticmethod
    def get_parsing_examples():
        return """"""
        
    
def as_gb(value):
    if isinstance(value, HasComponents):
        return value  
    if isinstance(value, list):
        return PGList(map(as_gb, value))
    else:
        return PGNative(value)

