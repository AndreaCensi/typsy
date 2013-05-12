from sts import HasComponents
from contracts import contract


class Block(HasComponents):
    
    short = 'block'
    
    @contract(parameters='list(parameter)')
    def __init__(self, parameters):
        self.parameters = parameters
    
    def get_components(self):
        return ['parameters']
    
    def __str__(self):
        plist = ",".join(str(x) for x in self.parameters)
        return 'Config(%s)' % plist
    
