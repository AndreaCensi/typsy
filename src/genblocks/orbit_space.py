from contracts import contract
from genblocks.interfaces import Space
from sts import HasComponents
from genblocks.group_action import GroupAction

        
class OrbitSpace(Space, HasComponents):
    
    short = 'os'
    
    @contract(s=Space, g=GroupAction)
    def __init__(self, s, g):
        self.space = s
        self.group = g 
    
    def belongs(self, a):
        return self.S.belongs(a)
        
    def equals(self, a, b):
        return self._group.related(a, b)
    
    def __str__(self):
        return '(%s)/(%s)' % (self.space, self.group)

    @staticmethod
    def get_parsing_expr():
        return None

