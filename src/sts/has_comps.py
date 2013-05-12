from contracts import contract
from contracts.main import get_all_arg_names
from sts.exceptions import FailedMatch, NotMatch
from abc import ABCMeta


class HasMeta(type):
    aliases = []
    tmp_config = []
    tmp_input = []
    tmp_output = []

    def __init__(cls, clsname, bases, clsdict):  # @UnusedVariable
        # Do not do this for the superclasses 
        if clsname in ['HasComponents']:
            return
        short = cls.short
        HasComponents.klasses[short] = cls
        

class HasComponents():

    """ Has components """
    
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
                self.debug('%r is not a HasComponents' % k)
        return cv
    
    def match(self, variables, other):
        self.debug('match generic (vars: %s, other=%s)' % (variables, other))
        if not type(self) == type(other):
            raise FailedMatch(self, other)
        comps = self.get_components()
        spec = dict([k, other.__dict__[k]] for k in comps)
        self.match_components(variables, spec)
        
    def __eq__(self, other):
        if not type(self) == type(other):
            self.debug('different type')
            return False 
        for k, a in self.get_components_values().items():
            b = other.__dict__[k]
            try:
                e = a.__eq__(b) 
            except AttributeError:
                e = a == b 
            if not e:
                self.debug('component %r does not match' % k)
                self.debug('a: %r' % a)
                self.debug('b: %r' % b)
                return False
        return True
        
    @contract(variables=dict, spec=dict)
    def match_components(self, variables, spec):
        """
            pattern matching
        """
        self.debug('match_components (vars: %s, spec=%s)' % (variables, spec))
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
        self.debug('replace_vars')
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
    
    def debug(self, s):
        print(' ' * (1 + HasComponents.debug_level) + '-' + (' %60s ' % self) + (s))
              
    debug_level = 0
    klasses = {}
    names = {}
     
def sts_symbol(n, s):
    HasComponents.names[n] = s 
 
# def sts_class(k):
#     HasComponents.klasses[k.short] = k
#     return k



