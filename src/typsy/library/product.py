# -*- coding: utf8 -*-
from genblocks import contract_inherit
from genblocks.interfaces import Space

from typsy.special import PGList
from typsy.parseables import ParseableWithOperators


class ProductSpace(ParseableWithOperators, Space):
    short = 'product'
    
    @staticmethod
    def get_arity():
        return ParseableWithOperators.TWO_OR_MORE

    @staticmethod
    def get_glyphs():
        return ["×", "x"]
    
    def __init__(self, *spaces):
        self.spaces = PGList(spaces)
          
    @contract_inherit
    def belongs(self, a):
        bel = [s.belongs(x) for s, x in zip(self.spaces, a)] 
        return all(bel)
    
    @contract_inherit  
    def equals(self, a, b):
        """
            raises: NotBelongs
        """
        pass

    def __repr__(self):
        return 'ProductSpace(%r)' % self.spaces
        
    @staticmethod
    def get_parsing_examples():
        return """
        $A x $B
        ($A x $B) -> $C

        """ 
