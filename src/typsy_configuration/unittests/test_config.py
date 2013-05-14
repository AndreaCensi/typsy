# import unittest
# from sts import parse_yaml_spec
# from contracts import contract
# 
# class Component:
#   
#     @contract(param1='int', param2='int')
#     def __init__(self, param1, param2):
#         pass
#     
#     def get_type(self):
#         pass
#     
# comp_spec = ("""
# # A representation nuisance is a map   
# map:
#   # from a valid configuration
#   i:
#     config:
#      parameters:
#      - param:
#          name: values
#          contract: none|int,>=1
#      - param:
#          name: values
#          contract: none|int,>=1
#   o:
#    # and creates a method that 
#    map:
#     # given a bootspec
#     i:  
#      bb:
#       i: 
#         prod:
#          s: $S
#          n: $N
#       o: $Y
#       t: $t
#      # gives a filter
#     o: 
#      bb:  
#       i: 
#         prod:
#          s: $S
#          n: $N
#       o: 
#         prod:
#          s: $S
#          n: $N
#       t: $t
# """)
#  
# 
# class TestConfig(unittest.TestCase):
#     def test1(self):
#         res = parse_yaml_spec(comp_spec)
#         print res
#         
