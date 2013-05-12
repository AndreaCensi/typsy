import unittest
from genblocks.parsing.parsin import parse_yaml_spec
from contracts import contract

class Component:
  
    @contract(param1='int', param2='int')
    def __init__(self, param1, param2):
        pass
    
    def get_type(self):
        pass
    
comp_spec = ("""
# A representation nuisance is a map   
map:
  # from a valid configuration
  i:
    configuration:
     parameters:
     - name: values
       contract: none|int,>=1
     - name: values
       valid: True
       contract: none|int,>=1
  o:
   # and creates a method that 
   map:
    # given a bootspec
    i:  
     bb:
      i: 
        product:
         space: $S
         n: $N
      o: $Y
      t: $t
     # gives a filter
    o: 
     bb:  
      i: 
      o: 
""")

spec_i = ("""
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

spec_o_expected = ("""
 sp: 
    o:  
      product:
       spaces:
       - bit
       - bit
""")

class TestConfig(unittest.TestCase):
    def test1(self):
        res = parse_yaml_spec(comp_spec)
        print res
        
