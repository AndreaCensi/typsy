# -*- coding: utf8 -*-
from typsy.special import PGList
from typsy.parseables import ParseableWithOperators

__all__ = ['Intersection']

class Intersection(ParseableWithOperators): 
     
    @staticmethod
    def get_arity():
        return ParseableWithOperators.TWO_OR_MORE

    @staticmethod
    def get_glyphs():
        return ["∩", "^"]
    
    def __init__(self, *spaces):
        if len(spaces) == 1:
            raise Exception()
        
        self.spaces = PGList(spaces)
    
    def belongs(self, a):
        raise NotImplemented
    
    def equals(self, a, b):
        raise NotImplemented

    def __repr__(self):
        return 'Intersection(%r)' % self.spaces
     
    def replace_vars(self, variables):
        if len(self.spaces) == 1:
            return self.spaces[0]
        else:
            return super(Intersection, self).replace_vars(variables)
    
    @staticmethod
    def get_parsing_examples():
        return """
        Space ^ Numeric
        """
        
    def reduce(self):
        spaces = [c.reduce() for c in self.spaces]
        flattened = flatten_inter(spaces)
        reduced = reduce_intersection(flattened)
        if len(reduced) == 1:
            return reduced[0]
        else:
            return Intersection(*reduced) 
            
            
def reduce_intersection(spaces):
    """
        spaces: list of spaces
        returns the minimal way to describe the intersection
    """
    return remove_doubles(spaces)

def remove_doubles(ss):
    res = []
    for s in ss:
        if not s in res:
            res.append(s)
    return res
    

def flatten_inter(spaces):    
    flattened = []
    
    def alls():
        for s in spaces:
            if isinstance(s, Intersection):
                for x in s.spaces:
                    yield x
            else:
                yield s
    
    for x in alls():
        flattened.append(x)
    return flattened

        
