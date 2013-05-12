from contracts import contract
from genblocks.interfaces import Space, HasComponents
from genblocks.group_action import GroupAction

        
class OrbitSpace(Space, HasComponents):
    
    @contract(s=Space, g=GroupAction)
    def __init__(self, s, g):
        self.space = s
        self.group = g 
    
    def belongs(self, a):
        return self.S.belongs(a)
        
    def equals(self, a, b):
        return self._group.related(a, b)
    
    def __str__(self):
        return '(%s)/(%s)' % (self._space, self._group)

    def get_components(self):
        return ['space', 'group']
