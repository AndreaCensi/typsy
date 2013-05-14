from typsy.parseables import ParseableWithExpression
 

class StochasticProcess(ParseableWithExpression):
    
    # @contract(o=Space)
    def __init__(self, o, t):
        self.o = o
        self.t = t
        
    def __repr__(self):
        return 'StochasticProcess(%r,%r)' % (self.o, self.t)


    def belongs(self, a):
        raise NotImplemented

    def equals(self, a, b):
        return a == b
 
    @classmethod
    def get_identifier(cls):
        return 'SP'


    @staticmethod
    def get_parsing_examples():
        return """
        SP({1};$t)
        SP({1,2};$t)
        """


