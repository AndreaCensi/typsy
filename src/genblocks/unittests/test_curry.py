# -*- coding: utf8 -*-
from sts.parsing.parsin import parse_spec

 
def test_demo():
    # Given a function of type f(AxBxC)-> N
    # currying produces curry(f):A->(B->(C->N)) 
 
    # Given a function of type f(AxB)-> N
    # currying produces curry(f):A->(B->N) 
    T = parse_spec
     
    curry_type = T('((($A)x($B))->($N))->(($A)->(($B)->($N)))')
    f_type = T("(({0,1})x({2,2}))-> ({2,3})")
    res_type = curry_type(f_type)
    print('res: %s' % res_type)
     

def test_demo2():
    # Given a function of type f(AxBxC)-> N
    # currying produces curry(f):A->(B->(C->N)) 

    # Given a function of type f(AxB)-> N
    # currying produces curry(f):A->(B->N) 
    T = parse_spec
    # 
    
    curry_type = T('((A×B)→N) → (A→(B→N))')
    
    f_type = T("({0,1} × X) → {2,4}")
    res_type = curry_type(f_type)
    
    print('   curry: %s' % curry_type)
    print('       f: %s' % f_type)
    print('curry(f): %s' % res_type)
    
