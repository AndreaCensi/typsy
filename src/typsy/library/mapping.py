# -*- coding: utf8 -*-
from .product import ProductSpace
from .space import Space
from typsy.interface import TypsyType, get_typsy_type
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
        return ["⟶", "→", "->"]
        
    def __init__(self, i, o):
        self.i = i
        self.o = o

    def __call__(self, *args):
        return self.call(args, different_scope=True)
    
    def call(self, args, different_scope=True):
        """
            If different_scope is True, then it is assumed that the scope
            of the input variables is different. For example, if the 
            two inputs are: 'Sequences(A)' and 'Sequences(A)', it
            is assumed that 'A' is different in either.
        """
        # First, lets get types if they are not already
        def map_to_type(x):
            if isinstance(x, TypsyType):
                return x
            else:
                return get_typsy_type(x)
        args = map(map_to_type, args)
        
        # let's honor different_scope
        if different_scope:
            args = make_different_scope(args)
        
        if len(args) == 1:
            i = args[0]
        else:
            i = ProductSpace(*tuple(args))
            
        precedence_ours = False
        
        if precedence_ours:
            # change the input such that they don't use variables
            # that we use internally
            my_variables = self.get_variables()
            already_taken = self.get_variables() | i.get_variables()
            i = i.replace_used_variables(already_taken=already_taken, substitutions={})
             
            if True:
                # double check
                his_variables = i.get_variables()
                common = my_variables & his_variables
                assert not common, (my_variables, his_variables)
               
            variables = {}
            res = self.match_components(variables, dict(i=i))
            spec_o = res['o']
            return spec_o.reduce()
        
        else:
            his_variables = i.get_variables()
            already_taken = self.get_variables() | i.get_variables()
            us = self.replace_used_variables(already_taken=already_taken, substitutions={})
            print('us:  %s' % self)
            print('us2: %s' % us)
            variables = {}
            res = us.match_components(variables, dict(i=i))
            spec_o = res['o']
            return spec_o.reduce()

            
            
    def __repr__(self):
        return 'Mapping(%r, %r)' % (self.i, self.o)

    @staticmethod
    def get_parsing_examples():
        return """
        ({0}) -> ({1})
        ({0})->(({0})->({1}))

        """

def make_different_scope(args):
    already_taken = set()
    for a in args:
        already_taken.update(a.get_variables())
        
    args2 = []
    for a in args:
        a2 = a.replace_used_variables(already_taken, substitutions={})
        args2.append(a2)
        already_taken.update(a2.get_variables())

    # print('scope: %s -> %s' % (args, args2))
    return args2


