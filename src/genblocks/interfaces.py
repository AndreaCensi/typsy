from contracts import contract, new_contract
from abc import abstractmethod, ABCMeta

class Serialized():
    __metaclass__ = ABCMeta
    
#     @abstractmethod
#     def to_struct(self):
#         pass

@new_contract
def space(x):
    pass

@new_contract
def in_input(x):
    pass

@new_contract
def in_output(x):
    pass

@new_contract
def in_space(x):
    pass

class NotMatch(Exception):
    def __init__(self, msg, context=[]):
        self.context = context
        self.msg = msg
        Exception.__init__(self, msg)
        
class FailedMatch(NotMatch):
    def __init__(self, me, other):
        self.me = me
        self.other = other
        msg = 'Could not match:'
        msg += '\n spec %s' % me  
        msg += '\n with %s' % other
        NotMatch.__init__(self, msg)
        

class HasComponents():

    """ Has components """
    __metaclass__ = ABCMeta
    
    @abstractmethod
    @contract(returns='list(str)')
    def get_components(self):
        """ Returns members of the structure """ 

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
        for k in self.get_components():
            a = self.__dict__[k]
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
        comps = self.get_components()
        toformat = []
        for k in comps: 
            if not k in spec:
                toformat.append(k)
        for k2 in spec:
            if not k2 in comps:
                msg = 'not %r in %r' % (k2, comps)
                raise NotMatch(msg)
        for k in comps:
            c = self.__dict__[k]
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
            if isinstance(c, HasComponents):
                HasComponents.debug_level += 1
                kwargs[k] = c.replace_vars(variables)
                HasComponents.debug_level -= 1
            else:
                kwargs[k] = c
        return klass(**kwargs)
    
    def debug(self, s):
        print(' ' * (1 + HasComponents.debug_level) + '-' + ' %60s ' % self +s)
             
    def __repr__(self):
        return self.__str__()
    
    
    debug_level = 0


class NotBelongs():
    @contract(space='space')
    def __init__(self, space, a):
        pass

class Space(Serialized):
    # TODO: should be called Set
    __metaclass__ = ABCMeta
        
    @abstractmethod    
    def belongs(self, a):
        pass

    @abstractmethod    
    def equals(self, a, b):
        """
            raises: NotBelongs
        """
        pass


class EquivRelation():
    __metaclass__ = ABCMeta
    
    @contract(S=Space)
    def __init__(self, S):
        self._space = S

    @abstractmethod    
    @contract(a='in_space', b='in_space', returns='bool')
    def related(self, a, b):
        pass


class Mapping(Serialized, HasComponents):
    __metaclass__ = ABCMeta
    
    @contract(i=Space, o=Space)
    def __init__(self, i, o):
        self.i = i
        self.o = o

    @contract(v='in_input', returns='in_output')
    def __call__(self, v):
        pass
    
    def to_struct(self):
        return {'i': self.i, 'o': self.o}
    
    def __str__(self):
        return "(%s)->(%s)" % (self.i, self.o)
    
    def get_components(self):
        return ['i', 'o']
   
