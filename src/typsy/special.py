from typsy.has_comps import HasComponents
from typsy.natives import PGNative

    
class PGList(list, HasComponents):
    
    def __init__(self, iterable):
        for c in iterable:
            if not isinstance(c, HasComponents):
                msg = 'element  %r is not Hascomponents' % c
                raise ValueError(msg)
            
        list.__init__(self, iterable)
        
    def match(self, variables, other):
        for s1, s2 in zip(self, other):
            HasComponents.debug_level += 1
            s1.match(variables, s2)
            HasComponents.debug_level -= 1
    
    @classmethod
    def get_components(klass):  # @UnusedVariable
        return []
    
    def reduce(self):
        return PGList([c.reduce() for c in self])

    def get_variables(self):
        variables = set()
        for v in self:
            variables.update(v.get_variables())
        return variables

    def _recursive_create(self, f):
        repl = []
        for x in self:
            x2 = f(x)
            repl.append(x2)
        return PGList(repl) 

#     new_values = dict([(k, f(c)) 
#                            for k, c in self.get_components_and_values()])
#         try:
#             return type(self).create_from_kwargs(**new_values)
#         except (Exception, TypeError) as e:
#             msg = 'Could not call create_from_kwargs for %r' % type(self)
#             msg += '\n values: %s' % new_values
#             msg += '\n' + indent(traceback.format_exc(e), '> ')
#             raise Exception(msg)

# 
#     def replace_vars(self, variables):
#         repl = []
#         for c in self:
#             if not isinstance(c, HasComponents):
#                 msg = 'I am a list:\n%s\n' % self
#                 msg += 'element  %r is not Hascomponents' % c
#                 raise ValueError(msg)
#             c2 = c.replace_vars(variables)
#             if not isinstance(c, HasComponents):
#                 msg = 'Replacement is not HasComponetns:\n'
#                 msg += ' c: %s\n' % c
#                 msg += ' c2: %s\n' % c2
#             repl.append(c2)
#         return PGList(repl)

    @staticmethod
    def get_parsing_expr():
        return None
    
    @staticmethod
    def get_parsing_examples():
        return """"""
        
    
def as_gb(value):
    if isinstance(value, HasComponents):
        return value  
    if isinstance(value, list):
        return PGList(map(as_gb, value))
    else:
        return PGNative(value)

