from typsy.library.space import Space
from typsy.has_comps import ParseableAsString


class Numeric(Space, ParseableAsString):
    short = 'numeric'

    def __init__(self):
        pass

    @staticmethod
    def get_parsing_examples():
        return """
        Numeric
        Numeric -> Numeric
        """
 
    @classmethod
    def get_identifier(klass):  # @UnusedVariable
        return 'Numeric'

    def __repr__(self):
        return 'Numeric()'
    
    
    
