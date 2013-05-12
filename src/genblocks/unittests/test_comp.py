from genblocks.common import ConstantMapping, bit
import unittest


class TestConstantMapping(unittest.TestCase):        
    def test1(self):
        S = bit
        f = ConstantMapping(i=S, o=S, value=0)
        assert f(0) == 0
        assert f(1) == 0
                   
class TestCompositions(unittest.TestCase):        

    def test_composition1(self):
        g = ConstantMapping(bit, bit, 0)
        g = ConstantMapping(bit, bit, 1)
    
        # Compose.eval(g, g2)
