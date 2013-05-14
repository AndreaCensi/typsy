# -*- coding: utf8 -*-

from typsy import HasComponents, TypsyGlobals
from genblocks import contract_inherit
from contracts import contract
from genblocks.interfaces import Space
from pyparsing import Literal, Suppress, ZeroOrMore
from typsy.has_comps import sts_type, simple_sts_type, ParseableWithOperators

from typsy.special import PGList



class ProductSpace(Space, ParseableWithOperators):
    short = 'product'
    
    @contract(spaces='seq[>=1](space)')
    def __init__(self, spaces):
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
    def get_parsing_expr():
        S = Suppress
        inside = simple_sts_type ^ (S('(') - sts_type - S(')'))  

        times = S(Literal('x') | Literal('×'))
        expr = inside + times - inside + ZeroOrMore(times - inside) 
        
        def parse_action(s, loc, tokens):  # @UnusedVariable
            values = list(tokens)
            return ProductSpace(values)
            
        expr.setParseAction(parse_action)
        expr.setName('product')
        
        return False, expr
        
    @staticmethod
    def get_parsing_examples():
        return """
        $A x $B
        ($A x $B) -> $C

        """

    def __str__(self):
        if TypsyGlobals.use_unicode:
            glyph = ' × '
        else:
            glyph = ' x '

        return glyph.join(map(self.format_sub, self.spaces)) 

