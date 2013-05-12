from sts import HasComponents
from contracts import contract, new_contract

class Parameter(HasComponents):
    
    short = 'param'
    
    @contract(name=str, required=bool, contract=str)
    def __init__(self, name, contract, required=False):
        self.name = name
        self.required = required
        self.contract = contract

    def __str__(self):
        return '%s:%s' % (self.name, self.contract)
    
new_contract('parameter', Parameter)
    
class Configuration(HasComponents):
    
    short = 'config'
    
    @contract(parameters='list(parameter)')
    def __init__(self, parameters):
        self.parameters = parameters

    def __str__(self):
        plist = ",".join(str(x) for x in self.parameters)
        return 'Config(%s)' % plist
    
    
#     
#     
# 'configuration': {'parameters': [{'contract': 'none|int,>=1',
#                                                  'name': 'values'},
#                                                 {'contract': 'none|int,>=1',
#                                                  'name': 'values',
#                                                  'valid': True}]}},
