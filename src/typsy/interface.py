from contracts import ContractsMeta
from contracts import contract, new_contract, describe_value
from abc import abstractmethod
from .utils import make_generic_decorator

class TypsyAssignments(dict):
    pass

class TypsyException(Exception):
    pass

class ValueNotInType(TypsyException):
    def __init__(self, tt, value):
        self.tt = tt
        self.value = value
        msg = 'Value not in type.\n- value: %s\n - type: %s' % (value, tt)
        TypsyException.__init__(self, msg)


def is_typsy_type(x):
    return isinstance(x, TypsyType)

new_contract('TypsyType', is_typsy_type)
    
class TypsyType(object):
    __metaclass__ = ContractsMeta

        
    @contract(returns=TypsyAssignments)
    def belongs(self, value):
        """ 
            Checks whether the value belongs to this type. 
            Returns a dictionary with type assignments.
            or raises ValueNotInType 
        """ 
        tt = get_typsy_type(value)
        return self.match_expr(tt)

    def equals(self, a, b):
        """ 
            Checks whether two values are the same when seen
            through this type. 
        """
        return a == b

    @abstractmethod
    @contract(returns=TypsyAssignments, other='TypsyType')
    def match_expr(self, other):
        """
        
        """ 



@make_generic_decorator
def typsy_type(f, typsy_type):
    """ Describes the decorator of a function. """
    # print('decorating:\n f = %r\n typsy_type: %r' % (f, typsy_type))
    from typsy.parsing.parsin import parse_spec
    tt = parse_spec(typsy_type)
    set_typsy_type(f, tt)
    return f

attrname = '__typsy_type__'
funcname = 'get_typsy_type'

@contract(returns=TypsyType)
def get_typsy_type(x):
    """ 
        Returns the type of the object x.
        
        There are multiple options that are checked in sequence:
        
        1) The object has a '__typsy_type__' attribute.
        
        2) The object has a callable attribute 'get_typsy_type()'.
        
        3) TODO: the object is a function and it has been decorated
           using contracts.
    """
    if hasattr(x, attrname):
        return getattr(x, attrname)
    elif hasattr(x, funcname):
        func = getattr(x, funcname)
        return func()  # it is already bound
    else:
        msg = 'Could not get typsy type for object.' 
        msg += '\n - object %r' % describe_value(x)
        raise TypsyException(msg) 
    


@contract(tt='str|TypsyType')
def set_typsy_type(x, tt):
    """ 
        Sets the type of the object x.
    """
    if isinstance(tt, str):
        from typsy.parsing.parsin import parse_spec
        tt = parse_spec(tt)

    setattr(x, attrname, tt)



