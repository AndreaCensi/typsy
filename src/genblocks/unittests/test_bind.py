# -*- coding: utf8 -*-
from sts.parsing.parsin import parse_spec
from sts.has_comps import format_variables


def test_bind3():
    T = parse_spec
    t1 = T('SP(A;1)')
    t2 = T('C')
    m = t1.match_expr(t2)
    print format_variables(m)
    assert len(m) == 1 
    assert m['C'] == T('SP(A;1)')


def test_bind4():
    T = parse_spec
    t1 = T('A->(B x A)')
    t2 = T('C->({0,2}x{0,1})')
    print t1
    print t2
    m = t1.match_expr(t2)
    print format_variables(m)
    assert len(m) == 2
    assert m['A'] == T('C∩{0,1}')
    assert m['B'] == T('{0,2}')
    # assert m['C'] == T('{0,1}')

def test_bind5():
    T = parse_spec
    t1 = T('A x A')
    t2 = T('C x {0,2}')
    m = t1.match_expr(t2)
    print
    print t1
    print t2
    print format_variables(m)
    assert len(m) == 1
    assert m['A'] == T('C∩{0,2}') 


def test_bind6():
    T = parse_spec
    t1 = T('C x {0,2}')
    t2 = T('A x A')
    m = t1.match_expr(t2)
    print
    print t1
    print t2
    print format_variables(m)
    assert len(m) == 2 
    assert m['A'] == T('{0,2}')
    assert m['C'] == T('{0,2}')

test_bind4.this = 1
