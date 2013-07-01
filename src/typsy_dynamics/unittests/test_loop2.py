# -*- coding: utf8 -*-
import unittest
from typsy import parse as T


# (P((BB(U;Y;t))x(BB(Y;U;t))))->(SP(P((Y)x(U))))
# BB(U;Y;t) x BB(Y;U;t)-> SP(P(YxU))

class TestLoop(unittest.TestCase):
    def test1(self):
        loop_spec = T('(BB(B;A;t) x BB(A;B;t)) -> SP(A x B;t)')
        spec_i = T('BB({0,2};{0,1};t) x BB({0,1};{0,2};t)')
        spec_o_expected = T('SP({0,1}x{0,2};t∩ Numeric)') 
        
        spec_o = loop_spec(spec_i)


        def prints(what, x):
            print('%15s: %s' % (what, x))
            
        prints('loop', loop_spec)
        prints('spec_i', spec_i)
        prints('spec_o_expected', spec_o_expected)
        prints('spec_o', spec_o)

        assert spec_o.equal_up_to_names(spec_o_expected)
                
        # self.assertEqual(spec_o_expected, spec_o) 
        
        
