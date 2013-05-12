from sts import HasComponents
from sts.exceptions import FailedMatch


class Variable(HasComponents):
    short = 'variable'
    
    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return '$' + self.name

    def get_components(self):
        return []
    
    def match(self, variables, other):
        self.debug('match (vars: %s)' % variables)
        if self.name in variables:
            v = variables[self.name]
            self.debug('variable already found = %s' % v)
            if v == self:
                self.debug('variable is me!')
                return  # XXX 
                # raise ValueError()
            if isinstance(v, HasComponents):
                HasComponents.debug_level += 1
                v.match(variables, other)
                HasComponents.debug_level -= 1
            else:
                if v != other:
                    raise FailedMatch(v, other) 
        else:
            self.debug('Setting variable to %s' % other)
            variables[self.name] = other

    def replace_vars(self, variables):
        self.debug('replace_vars')
        return variables[self.name]
