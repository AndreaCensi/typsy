from typsy.has_comps import HasComponents
from typsy.parseables import ParseableAsString

class Space(HasComponents):
    short = 'space'

    def __init__(self):
        pass
    
#     @staticmethod
#     def get_parsing_examples():
#         return ""
#  
#     def __repr__(self):
#         return 'Space()'
#     
#     def __str__(self):
#         return 'Space'
#     

class Space2(ParseableAsString, HasComponents):

    def __init__(self):
        pass
    
    @staticmethod
    def get_parsing_examples():
        return ""
 
    @classmethod
    def get_identifier(klass):
        return 'Space'

    def __repr__(self):
        return 'Space2()'
    
    def __str__(self):
        return 'Space'
    
#     @staticmethod
#     def get_parsing_expr():
#         S = Suppress
#         L = Literal
#         expr = (S(L('Space')))
#         expr.setName('Space')
#          
#         def parse_action(s, loc, tokens):  # @UnusedVariable
#             # print('tokens: %r' % tokens)
#             return Space()
#          
#         expr.setParseAction(parse_action)
#         return True, expr

# 
# class NotBelongs():
#     @contract(space=Space)
#     def __init__(self, space, a):
#         pass
# #     
# class ConcreteSpace(Space):
#     @abstractmethod     
#     def belongs(self, a):
#         pass
#     
#     @abstractmethod
#     def equals(self, a, b):
#         pass

