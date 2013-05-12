import unittest
from genblocks.parsing.parsin import parse_yaml_spec

# (P((BB(U;Y;t))x(BB(Y;U;t))))->(SP(P((Y)x(U))))
# BB(U;Y;t) x BB(Y;U;t)-> SP(P(YxU))



class TestLoop(unittest.TestCase):
    def test1(self):
        loop_spec_s = ("""
        # A loop is a map 
        map:
          i:
          # that takes two black boxes
            product:
             spaces:
             - bb:  # agent
                 t: $t
                 i: $Y
                 o: $U
             - bb: 
                 t: $t
                 i: $U
                 o: $Y
          o:
          # and creates a stochastic process in the product space
            sp: 
             o: 
              product:
               spaces:
               - $Y
               - $U
             t: $t
        """)
        
        spec_i_s = ("""
        product:
         spaces:
         - bb: # agent
            i: bit
            o: bit
            t: 1
         - bb: 
            i: bit
            o: bit
            t: 1
        """)
        
        spec_o_expected_s = ("""
         sp: 
            o:  
              product:
               spaces:
               - bit
               - bit
            t: 1
        """)
        
        loop_spec = parse_yaml_spec(loop_spec_s)
        spec_i = parse_yaml_spec(spec_i_s)
        spec_o_expected = parse_yaml_spec(spec_o_expected_s)
        
        variables = {}
        res = loop_spec.match_components(variables, dict(i=spec_i))
        spec_o = res['o']
        
        print 'variables', variables
        
        self.assertEqual(spec_o_expected, spec_o) 
        
        
