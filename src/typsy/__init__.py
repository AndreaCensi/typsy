"""

    Type algebra
    ------------
    
    
        T1 <= T2
        
        <= : Type x Type -> bool
        >= 
        
    
    Matching types
    
    
    t1 = Numeric
    t2 = Integer
    
    t1 >= t2
    
    try:
        res = t.match_expr(t2)
    except NotMatch:
        ...
        
    Interacting with values: ::
    
        @type('Int -> Int')
        def f(x):
            return x + 2

    
        @type('Int -> Int')
        def f(f2):
            return lambda x: f(x)

    Using types with objects
    ------------------------
    
    Setting types for objects: ::
    
        typsy_type(f, 'Int->Int')
    
    This parses the definition and puts it inside the '__typsy__'
    variable. 
    
    Getting types: ::
    
        typsy_get_type(f) #=> Int->Int
    
    Verifying types: ::
        
        t = typsy.parse('Int')
        1 in t # => True
    
    Verifying 
    
        typsy_get_type(f) #=> Int->Int
         

"""
__all__ = ['parse', 'Typsy', 'HasComponents']


class TypsyGlobals(object):
    use_unicode = True  

from .has_comps import get_sts_type, sts_type, HasComponents, simple_sts_type, sts_symbol
from . import intersection
from . import variable
from .library import *
from .parsing.parsin import parse_spec as parse


