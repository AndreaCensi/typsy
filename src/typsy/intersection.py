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
        return ["^", "∩"]
    
    def __init__(self, *spaces):
        flattened = []
        
        def alls():
            for s in spaces:
                if isinstance(s, Intersection):
                    for x in s.spaces:
                        yield x
                else:
                    yield s
        
        for x in alls():
            if not x in flattened:
                flattened.append(x)
                    
        self.spaces = PGList(flattened)
    
    def belongs(self, a):
        raise NotImplemented
    
    def equals(self, a, b):
        raise NotImplemented

    def __repr__(self):
        return 'Intersection(%r)' % self.spaces
     
    @staticmethod
    def get_parsing_examples():
        return """
        Space ^ Numeric
        """
