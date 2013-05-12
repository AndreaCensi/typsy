
from sts import HasComponents
from genblocks import contract_inherit
from contracts import contract
from genblocks.interfaces import Space


class Product(Space, HasComponents):
    short = 'prod'
    
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
    short = 'product'
    
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

