# -*- coding: utf8 -*-
from typsy.library.space import Space
from typsy.parseables import ParseableWithOperators

__all__ = ['Mapping']


class Mapping(ParseableWithOperators): 
     
    @staticmethod
    def get_arity():
        return 2

    @staticmethod
    def get_subs():
        return [('i', Space()), ('o', Space())]

    @staticmethod
    def get_glyphs():
        return ["->", "→", "⟶"]
        
    def __init__(self, i, o):
        self.i = i
        self.o = o

    def __call__(self, i):
        variables = {}
        res = self.match_components(variables, dict(i=i))
        spec_o = res['o']
        return spec_o
    
    def __repr__(self):
        return 'Mapping(%r, %r)' % (self.i, self.o)

    @staticmethod
    def get_parsing_examples():
        return """
        ({0}) -> ({1})
        ({0})->(({0})->({1}))

        """
