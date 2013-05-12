# -*- coding: utf8 -*-

from sts import HasComponents
from genblocks import contract_inherit
from contracts import contract
from genblocks.interfaces import Space
from pyparsing import Literal, Suppress, ZeroOrMore
from sts.has_comps import sts_type, simple_sts_type
from sts.natives import PGList


class Product(Space, HasComponents):
    short = 'prod'
    
    @contract(s=Space, n=HasComponents)
    def __init__(self, s, n):
        self.s = s
        self.n = n
        
    @contract_inherit
    def belongs(self, a):
        bel = [s.belongs(x) for s, x in zip(self._spaces, a)] 
        return all(bel)
    
    @contract_inherit  
    def equals(self, a, b):
        """
            raises: NotBelongs
        """
        pass

    def __repr__(self):
        return 'Product(%r,%r)' % (self.s, self.n)
    
    def __str__(self):
        return '(%s)^%s' % (self.s, self.n)


    @staticmethod
    def get_parsing_expr():
        S = Suppress
        inside = (S('(') - sts_type - S(')')) | simple_sts_type

        expr = inside + Suppress(Literal('^')) - inside

        def parse_action(s, loc, tokens):  # @UnusedVariable
            try:
                s = tokens[0]
                n = tokens[1]
                return Product(s, n)
            except Exception as e:
                print e
            
        expr.addParseAction(parse_action)
        expr.setName('prod')

        return False, expr



class ProductSpace(Space, HasComponents):
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
#                 def convert(x):
#             if isinstance(x, Binary) and x.precedence < self.precedence:
#                 return '(%s)' % x
#             else:
#                 return '%s' % x

#         s = self.glyph.join(convert(x) for x in self.exprs)
#         return s

        return "x".join('(%s)' % s for s in self.spaces) 

