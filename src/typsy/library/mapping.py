# -*- coding: utf8 -*-
from typsy import   TypsyGlobals
from typsy.has_comps import ParseableWithOperators

__all__ = ['Mapping']


class Mapping(ParseableWithOperators): 
     
    @staticmethod
    def get_arity():
        return 2

    @staticmethod
    def get_glyphs():
        return ["⟶", "->"]
        
    short = 'map'
    
    # @contract(i=Space, o=Space)
    # TODO: generic
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
#     
#     def __str__(self):
#         i = '%s' % self.i
#         o = '%s' % self.o
#         
#         if self.i.get_precedence() <= self.get_precedence():
#             i = '(%s)' % i
#         if self.o.get_precedence() <= self.get_precedence():
#             o = '(%s)' % o
#         
#         if TypsyGlobals.use_unicode:
#             return "%s ⟶ %s" % (i, o)
#         else:
#             return "%s -> %s" % (i, o)
# 
#     def get_precedence(self):
#         return -2
    
#     @staticmethod
#     def get_parsing_expr():
#         S = Suppress
#         inside = simple_sts_type | (S('(') - sts_type - S(')'))
#         
#         arrow = S(Literal('->') | Literal('→') | Literal('⟶'))
#         
#         expr = (inside + arrow - inside)
#         
#         def my_parse_action(s, loc, tokens):  # @UnusedVariable
#             i = tokens[0]
#             o = tokens[1]
#             return Mapping(i, o)
#                 
#         expr.addParseAction(my_parse_action)
#         expr.setName('mapping')
#         return False, expr
#     
    @staticmethod
    def get_parsing_examples():
        return """
        ({0}) -> ({1})
        ({0})->(({0})->({1}))

        """
