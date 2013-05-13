# -*- coding: utf8 -*-
from contracts import contract
from sts.has_comps import HasComponents, simple_sts_type, sts_type
from sts.natives import PGList
from sts import STSGlobals
from pyparsing import Suppress, Literal, ZeroOrMore


class Intersection(HasComponents):
    short = 'intersection'
    
    @contract(spaces='seq[>=1]')
    def __init__(self, spaces):
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
    def get_parsing_expr():
        S = Suppress
        inside = simple_sts_type ^ (S('(') - sts_type - S(')'))  

        glyph = S(Literal('∩') | Literal('∩'))
        expr = inside + glyph - inside + ZeroOrMore(glyph - inside) 
        
        def parse_action(s, loc, tokens):  # @UnusedVariable
            values = list(tokens)
            return Intersection(values)
            
        expr.setParseAction(parse_action)
        expr.setName('intersection')
        
        return False, expr
        
    @staticmethod
    def get_parsing_examples():
        return """
        Space ∩ Numeric
        """

    def __str__(self):

        if STSGlobals.use_unicode:
            glyph = ' ∩ '
        else:
            glyph = ' ∩ '

        return glyph.join(map(self.format_sub, self.spaces)) 

