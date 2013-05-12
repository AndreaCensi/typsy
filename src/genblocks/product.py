from genblocks.interfaces import Space, HasComponents, FailedMatch
from genblocks import contract_inherit
from contracts import contract


class Product(Space, HasComponents):
    def __init__(self, s, n):
        self.s = s
        self.n = n
        
    @contract_inherit
    def belongs(self, a):
        bel = [s.belongs(x) for s, x in zip(self._spaces, a)] 
        return all(bel)
    
    @contract_inherit  
    def equals(self, a, b):
        """
            raises: NotBelongs
        """
        pass

    def __str__(self):
        return '(%s)^%s' % (self.s, self.n)



class ProductSpace(Space, HasComponents):
    
    @contract(spaces='seq[>=1](space)')
    def __init__(self, spaces):
        self.spaces = spaces
          
    @contract_inherit
    def belongs(self, a):
        bel = [s.belongs(x) for s, x in zip(self.spaces, a)] 
        return all(bel)
    
    @contract_inherit  
    def equals(self, a, b):
        """
            raises: NotBelongs
        """
        pass

    def __repr__(self):
        return 'ProductSpace(%r)' % self.spaces
     
    def __str__(self):
#                 def convert(x):
#             if isinstance(x, Binary) and x.precedence < self.precedence:
#                 return '(%s)' % x
#             else:
#                 return '%s' % x

#         s = self.glyph.join(convert(x) for x in self.exprs)
#         return s

        return "x".join('(%s)' % s for s in self.spaces) 

    def get_components(self):
        return ['spaces']
    
    def match(self, variables, other):
        self.debug('match (vars: %s, other=%s)' % (variables, other))  
        if not isinstance(other, ProductSpace):
            raise FailedMatch(self, other)
            
        if len(other.spaces) != len(self.spaces):
            raise FailedMatch(self, other)
        
        for s1, s2 in zip(self.spaces, other.spaces):
            HasComponents.debug_level += 1
            s1.match(variables, s2)
            HasComponents.debug_level -= 1
  
    def replace_vars(self, variables):
        spaces = [s.replace_vars(variables) for s in self.spaces]
        return ProductSpace(spaces)
        
