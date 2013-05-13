from contracts import contract
from contracts.main import get_all_arg_names
from pyparsing import Forward, ParserElement, Or
from sts.exceptions import FailedMatch, NotMatch

ParserElement.enablePackrat()

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
        for cls in HasComponents.klasses.values(): 
            pexpr = cls.get_parsing_expr()
            if pexpr is not None:
                if not isinstance(pexpr, tuple):
                    msg = 'Could not %r' % cls
                    raise Exception(msg)
                simple, expr = pexpr
                try:
                    str(expr)
                except:
                    msg = 'invalid name for %r' % cls
                    raise ValueError(msg)
                if simple:
                    simple_exprs.append(expr)
                else:
                    complex_exprs.append(expr)
        simple_sts_type << Or(simple_exprs)
        sts_type << (simple_sts_type ^ Or(complex_exprs))
        sts_type_final = sts_type
        sts_type_final.setName('sts_type_final')
        return sts_type_final
    
class HasMeta(type):

    def __init__(cls, clsname, bases, clsdict):  # @UnusedVariable
        # Do not do this for the superclasses 
        if clsname in ['HasComponents']:
            return
        short = cls.short
        HasComponents.klasses[short] = cls
        if sts_type_final is not None:
            print('warning, adding %r but already created parsing' % short)
            

class HasComponents():
    """ 
        
        t1 = 'SP(A;1)'
        t2 = 'SP({0,1};1)'
        m = t1.match(t2) # {A=>{0,1}}
    
    """
    
    __metaclass__ = HasMeta
    
    @contract(returns='list(str)')
    def get_components(self):
        """ Returns members of the structure """
        x = get_all_arg_names(type(self).__init__)
        x.remove('self')
        return x 

    def get_components_values(self):
        cv = dict([(k, self.__dict__[k]) for k in self.get_components()])
        for k, v in cv.items():
            if not isinstance(v, HasComponents):
                # self.debug('%r is not a HasComponents' % k)
                pass
        return cv
    
    def match(self, variables, other):
        # self.debug('match generic (vars: %s, other=%s)' % (variables, other))
        from sts.variable import Variable
        if isinstance(other, Variable):
            variables[other.name] = self
            return True
        
        same = self.__class__ == other.__class__
        sub = issubclass(self.__class__, other.__class__)
        if not sub:
            msg = 'Could not match:\n'
            msg += '- self  %r\n' % self
            msg += '- other %r\n' % other
            msg += 'because classes dont match:\n'
            msg += '- self.class =  %s\n' % self.__class__ 
            msg += '- other.class =  %s\n' % other.__class__
            raise FailedMatch(self, other, msg)
        
        if same:
            comps = self.get_components()
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
        # self.debug('replace_vars')
        klass = type(self)
        comps = self.get_components()
        kwargs = {} 
        for k in comps:
            try:
                c = self.__dict__[k]
            except KeyError:
                raise Exception('no key %r in %s' % (k, self))
            
            HasComponents.debug_level += 1
            kwargs[k] = c.replace_vars(variables)
            HasComponents.debug_level -= 1
        
        return klass(**kwargs)
    
    @staticmethod
    def get_parsing_examples():
        return ""

    def get_variables(self):
        variables = {}
        for v in self.get_components_values().values():
            variables.update(v.get_variables())
        return variables
    
    def debug(self, s):
        print(' ' * (1 + HasComponents.debug_level) + '-' + (' %60s ' % self) + (s))
            
    debug_level = 0
    klasses = {}
    names = {}
     
    @staticmethod
    def get_parsing_expr():
        # Returns tuple Precedence, expression
        raise NotImplementedError()
    
    def get_precedence(self):
        simple, _ = type(self).get_parsing_expr()
        if simple: 
            return 1
        else:
            return 0
    
    def format_sub(self, x):
        """ returns either (x) or x whether one is needed """
        s = '%s' % x
        if x.get_precedence() <= self.get_precedence():
                s = '(%s)' % s
        return s
    
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
        msg += '\n- %5s: %s' % (k, v)
    return msg
    
def sts_symbol(n, s):
    HasComponents.names[n] = s 
  

