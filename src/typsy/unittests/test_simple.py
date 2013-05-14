# -*- coding: utf8 -*-
from typsy import parse as T
from typsy.unittests.test_parsing import check_example


def test_simple1():
#     check_example('A x B')
#     check_example('A x B -> C')
#     check_example('(A x B) -> C')
    check_example('Space')
    check_example('(Space) -> C')
    check_example('(Space -> C)')

    check_example('A -> B -> C')

    f_type = T("A -> B")
    f_type = T("A -> {2,4}")
    f_type = T("({0,1} × X) -> {2,4}")
    
    s = '((A x B)->N) -> (A->(B->N))'
    T(s)
    T(s.replace('->', '→'))
    
