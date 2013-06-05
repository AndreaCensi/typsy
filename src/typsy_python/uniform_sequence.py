from typsy.parseables import ParseableWithExpression
 

class UniformSequence(ParseableWithExpression):
    """ A sequence with objects in the same type. """ 
    
    def __init__(self, o):
        self.o = o
        
    def __repr__(self):
        return 'UniformSequence(%r)' % (self.o)

    def belongs(self, a):
        raise NotImplemented

    def equals(self, a, b):
        return a == b
 
    @classmethod
    def get_identifier(cls):
        return 'UniformSequence'

    @staticmethod
    def get_parsing_examples():
        return """
        UniformSequence($t)
        UniformSequence($t)
        """



