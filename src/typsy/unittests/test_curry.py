# -*- coding: utf8 -*-
from typsy import parse as T

 
def test_demo():
    # Given a function of type f(AxBxC)-> N
    # currying produces curry(f):A->(B->(C->N)) 
 
    # Given a function of type f(AxB)-> N
    # currying produces curry(f):A->(B->N) 
    curry_type = T('((AxB)->N)->(A->(B->N))')
    f_type = T("({0,1}x{2,2})-> ({2,3})")
    res_type = curry_type(f_type)
    print('res: %s' % res_type)
     

def test_demo2():
    # Given a function of type f(AxBxC)-> N
    # currying produces curry(f):A->(B->(C->N)) 

    # Given a function of type f(AxB)-> N
    # currying produces curry(f):A->(B->N) 
    
    T('{0,1}')
    T('{0,1} x X')
    T('{0,1} x X -> A')
    T('{0,1} x X -> Space')
    
    f_type = T("({0,1} × X) → {2,4}")
    curry_type = T('((A × B)→N) → (A→(B→N))')
    res_type = curry_type(f_type)
    
    print('   curry: %s' % curry_type)
    print('       f: %s' % f_type)
    print('curry(f): %s' % res_type)
    
