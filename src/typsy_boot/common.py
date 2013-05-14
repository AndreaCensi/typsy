from contracts import contract
from pyparsing import Literal
from typsy import FiniteSet, Space, sts_symbol, HasComponents, sts_type
from typsy_boot.product import Product


bit = FiniteSet([0, 1])

def bits(n):
    return Product(bit, n)                

sts_symbol('bit', FiniteSet([0, 1]))
# 
# class ConstantMapping(Mapping): 
#     short = 'constant'
#     
#     def __init__(self, i, o, value):
#         Mapping.__init__(self, i=i, o=o)
#         self.value = value
#         
#     @contract_inherit
#     def __call__(self, v):  # @UnusedVariable
#         return self.value 
    

