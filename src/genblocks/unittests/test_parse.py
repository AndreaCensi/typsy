import unittest
from sts import parse_yaml_spec

class TestParse(unittest.TestCase):
    def test1(self):
        s = \
"""
map:
  i:
    bb: 
     t: $t
     i: $in
     o: 
      os: 
       s: 
        prod:
            s: bit
            n: $n
       g: 
        gprod:
            s: bit
            n: $m
  o:
    bb: 
     t: $t
     i: $in
     o: 
      os: 
       s: 
        interval:
            bounds: [0,1]
       g: 
        aut:
            s: 
                interval:
                    bounds: [0,1]
                
"""
        r = parse_yaml_spec(s)
        print r
