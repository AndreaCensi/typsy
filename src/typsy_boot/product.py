
from genblocks import contract_inherit
from genblocks.interfaces import Space
from pyparsing import Literal, Suppress
from typsy import HasComponents, sts_type, simple_sts_type



class Product(Space, HasComponents):
    short = 'prod'
    
    # @contract(s=Space, n=HasComponents)
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

    def __repr__(self):
        return 'Product(%r,%r)' % (self.s, self.n)
    
    def __str__(self):
        return '(%s)^%s' % (self.s, self.n)


    @staticmethod
    def get_parsing_expr():
        S = Suppress
        inside = (S('(') - sts_type - S(')')) | simple_sts_type

        expr = inside + Suppress(Literal('^')) - inside

        def parse_action(s, loc, tokens):  # @UnusedVariable
            try:
                s = tokens[0]
                n = tokens[1]
                return Product(s, n)
            except Exception as e:
                print e
            
        expr.addParseAction(parse_action)
        expr.setName('prod')

        return False, expr
