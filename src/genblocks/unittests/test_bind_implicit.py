from sts.parsing.parsin import parse_spec
from sts.has_comps import format_variables
  
def test_bind_implicit1():
    T = parse_spec
    t1 = T('BB(A;{0,1};A)')
    # we should be able to get that A 
    # should be a Space and a number    
    t2 = T('BB(X;Y;Z)')
    print t1
    print t2

    m = t1.match_expr(t2)
    print format_variables(m)

  
