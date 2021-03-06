from .exceptions import FailedMatch, NotMatch
from .interface import TypsyType
from contracts import ContractsMeta, contract
from contracts.backported import getfullargspec
from contracts.interface import describe_type
from contracts.main import get_all_arg_names
from contracts.pyparsing_utils import myOperatorPrecedence
from contracts.utils import indent
from pyparsing import Forward, ParserElement, opAssoc, Suppress, Literal
from typsy.pyparsing_add import MyOr, wrap_parse_action
import traceback

ParserElement.enablePackrat()
# ParserElement.verbose_stacktrace = True

sts_type = Forward()
sts_type.setName('sts_type')
sts_type_final = None

simple_sts_type = Forward()

def get_sts_type():
    global sts_type_final
    if sts_type_final is not None:
        # print('reusing')
        return sts_type_final
    else:
        simple_exprs = []
        complex_exprs = []
        operators = []
        
        S = Suppress
        L = Literal

        for cls in HasComponents.klasses.values():
            from typsy.parseables import Parseable
            if not issubclass(cls, Parseable):
                # print('Warn, %r is not Parseable' % cls)
                continue 

            from typsy.parseables import ParseableWithOperators
            if issubclass(cls, ParseableWithOperators) and cls.get_arity() in [2]:
                glyphs = cls.get_glyphs()
                glyph = MyOr(map(L, glyphs))
                spec = (glyph, cls.get_arity(), opAssoc.LEFT,
                        wrap_parse_action(cls.op_system_parse_action)) 
                operators.append(spec)
            else:
                pexpr = cls.get_parsing_expr()
                if pexpr is not None:
                    if not isinstance(pexpr, tuple):
                        msg = 'Could not %r' % cls
                        raise Exception(msg)
                    simple, expr = pexpr
                    try:
                        str(expr)
                        # print cls, simple,str(expr) 
                        pass
                    except:
                        msg = 'invalid name for %r' % cls
                        raise ValueError(msg)
                    
                    if simple:
                        simple_exprs.append(expr)
                    else:
                        complex_exprs.append(expr)
                            
        # print('simple:    %r' % simple_exprs)
        # print('complex:   %r' % complex_exprs)
        # print('operators: %r' % operators)
        

        operand = (S('(') + sts_type + S(')')) | MyOr(complex_exprs + simple_exprs) 
        ops = myOperatorPrecedence(operand, operators)

        sts_type << ops
        
        simple_sts_type << MyOr(simple_exprs)
        
        sts_type_final = sts_type
        sts_type_final.setName('sts_type_final')
        
        return sts_type_final
    
    
class HasMeta(ContractsMeta):

    def __init__(cls, clsname, bases, clsdict):  # @UnusedVariable @NoSelf
        # Do not do this for the superclasses 
        if clsname in ['HasComponents', 'Parseable', 'ParseableWithOperators',
                       'ParseableWithExpression', 'ParseableAsString']:
            return

        HasComponents.klasses[cls.__name__] = cls
        
        if sts_type_final is not None:
            print('warning, adding %r but already created parsing' % cls)
            

class HasComponents(TypsyType):
    """ 
        
        t1 = 'SP(A;1)'
        t2 = 'SP({0,1};1)'
        m = t1.match(t2) # {A=>{0,1}}
    
    """
    
    __metaclass__ = HasMeta
    
    def __init__(self):
        pass
    
    @classmethod
    # @contract(returns='list(str)')
    def get_components(cls):
        """ Returns members of the structure """
        x = get_all_arg_names(cls.__init__)
        # XXX: looks like we changed something in contracts
        if 'self' in x:
            x.remove('self')
        return x
    
    def get_components_and_values(self):
        """ Returns members of the structure """
        components = type(self).get_components()
        for k in type(self).get_components():
            if not k in self.__dict__:
                msg = 'Object %r does not have %r' % (self, k)
                msg += '\n components: %r' % components
                raise Exception(msg)
            yield k, self.__dict__[k]

    def get_components_values(self):
        cv = dict([(k, self.__dict__[k]) for k in type(self).get_components()])
        for k, v in cv.items():
            if not isinstance(v, HasComponents):
                # self.debug('%r is not a HasComponents' % k)
                pass
        return cv
    
    @contract(other='TypsyType')
    def match(self, variables, other):
        # self.debug('match generic (vars: %s, other=%s)' % (variables, other))
        from typsy.variable import Variable
        if isinstance(other, Variable):
            variables[other.name] = self
            return True
        
        same = self.__class__ == other.__class__
        sub = issubclass(self.__class__, other.__class__)
        if not sub:
            msg = 'Could not match:\n'
            msg += '- self  %s\n' % self.__repr__()
            msg += '- other %s\n' % other.__repr__()
            msg += 'because classes dont match:\n'
            msg += '- self.class =  %s\n' % self.__class__ 
            msg += '- other.class =  %s\n' % other.__class__
            raise FailedMatch(self, other, msg)
        
        if same:
            comps = type(self).get_components()
            spec = dict([k, other.__dict__[k]] for k in comps)
            self.match_components(variables, spec)
    
    def match_expr(self, other):
        variables = {}
        self.match(variables, other)
        return reduce_vars(variables)
        
    def __eq__(self, other):
        if not type(self) == type(other):
            # self.debug('different type')
            return False 
        for k, a in self.get_components_values().items():
            b = other.__dict__[k]
            try:
                e = a.__eq__(b) 
            except AttributeError:
                e = a == b 
            if not e:
                # self.debug('component %r does not match' % k)
                # self.debug('a: %r' % a)
                # self.debug('b: %r' % b)
                return False
        return True
        
    @contract(variables=dict, spec=dict)
    def match_components(self, variables, spec):
        """
            pattern matching
        """
        # self.debug('match_components (vars: %s, spec=%s)' % (variables, spec))
        my_comps = self.get_components_values()
        
        toformat = []
        for k in my_comps: 
            if not k in spec:
                toformat.append(k)
                
        for k2 in spec:
            if not k2 in my_comps:
                msg = 'not %r in %r' % (k2, my_comps)
                raise NotMatch(msg)
            
        for k, c in my_comps.items():
            if not k in spec:
                continue
            
            HasComponents.debug_level += 1
            c.match(variables, spec[k])
            HasComponents.debug_level -= 1

        res = {}
        for k in toformat:
            c = self.__dict__[k]
            HasComponents.debug_level += 1
            res[k] = c.replace_vars(variables)
            HasComponents.debug_level -= 1
            
        return res
    
    def replace_vars(self, variables):
        f = lambda c: c.replace_vars(variables)
        return self._recursive_create(f)

    def reduce(self):
        f = lambda c: c.reduce()
        return self._recursive_create(f)

    @contract(returns='TypsyType')
    def _recursive_create(self, f):
        new_values = {}
        
        for k, c in self.get_components_and_values():
            c2 = f(c)
            if not isinstance(c2, TypsyType):
                msg = ('Could not transform %r (%s, %s) using %s: got %s' % 
                       (k, c, describe_type(c), f, describe_type(c2)))
                raise ValueError(msg)
            new_values[k] = c2
            
        try:
            return type(self).create_from_kwargs(**new_values)
        except (Exception, TypeError) as e:
            msg = 'Could not call create_from_kwargs for %r' % type(self)
            msg += '\n values: %s' % new_values
            msg += '\n' + indent(traceback.format_exc(e), '> ')
            raise Exception(msg)
            
     
    @classmethod
    def create_from_kwargs(klass, **kwargs):
        for k, v in kwargs.items():
            if not isinstance(v, TypsyType):
                msg = 'Expected a type for %r, got %s' % (k, describe_type(v))
                raise ValueError(msg)
        spec = getfullargspec(klass.__init__)
        if spec.varargs is None:
            return klass(**kwargs)
        else:
            # assert spec.args == ['self']
            assert spec.args == []
            assert len(kwargs) == 1
            values = list(kwargs.values())[0]
            return klass(*values)

    def get_variables(self):
        """ 
            Returns a set of names with the variables names used 
            in this expression. 
        """
        variables = set()
        for k, v in self.get_components_values().items():
            vs = v.get_variables()
            print('%s: %s' % (k, vs))
            variables.update(vs)
            
        return variables
    
    @contract(already_taken='set(str)', substitutions='dict(str:str)',
              returns='TypsyType')  # returns='tuple(*, dict(str:str) )')
    def replace_used_variables(self, already_taken, substitutions):
        """ 
            Returns a new type, where the variables have been substituted
            if they clashed with the already taken variables.
        """
        def replace(comp):
            return comp.replace_used_variables(already_taken, substitutions)
        return self._recursive_create(replace)
    
    def equal_up_to_names(self, other):
        """
             Checks that two types are the sames up to the names of variables.
             
             We can check this by substituting the variables with new names.
        """
        already_taken = self.get_variables() | other.get_variables()
        a = self.replace_used_variables(already_taken.copy(), substitutions={})
        b = other.replace_used_variables(already_taken.copy(), substitutions={})
        return a == b
        
    
    def debug(self, s):
        print(' ' * (1 + HasComponents.debug_level) + '-' + (' %60s ' % self) + (s))
            
    debug_level = 0
    klasses = {}
    names = {}
    
    
@contract(vs=dict, returns=dict)
def reduce_vars(vs):
    """
        {'A': Variable('C'), 'C': FiniteSet([PGNative(0), PGNative(2)])}
     => {'A': Variable('C'), 'C': FiniteSet([PGNative(0), PGNative(2)])}
    """
    vs = vs.copy()
    for k, v in vs.items():
        vs[k] = v.replace_vars(vs)
    return vs
        
@contract(variables='dict')
def format_variables(variables):
    """ Formats on multiline """
    msg = ''
    for k, v in variables.items():
        msg += '\n- %5s: %-35s   %r' % (k, v, v)
    return msg
    
def sts_symbol(n, s):
    HasComponents.names[n] = s 
  

