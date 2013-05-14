from typsy.has_comps import HasComponents
from typsy.exceptions import FailedMatch
from pyparsing import (delimitedList, Forward, Literal,  # @UnusedImport
  stringEnd, nums, Word, CaselessLiteral, Combine,  # @UnusedImport
  Optional, Suppress, OneOrMore, ZeroOrMore, opAssoc,  # @UnusedImport
  operatorPrecedence, oneOf, ParseException, ParserElement,  # @UnusedImport
  alphas, alphanums, ParseFatalException,  # @UnusedImport
  ParseSyntaxException, FollowedBy, NotAny, Or,  # @UnusedImport
  MatchFirst, Keyword, Group, White, lineno, col)  # @UnusedImport


O = Optional
S = Suppress
number = Word(nums)
point = Literal('.')
e = CaselessLiteral('E')
plusorminus = Literal('+') | Literal('-')
integer = Combine(O(plusorminus) + number)
floatnumber = Combine(integer + (point + O(number)) ^ (e + integer))
integer.setName('integer')
integer.setParseAction(lambda tokens: PGNative(int(tokens[0])))
floatnumber.setName('integer')
floatnumber.setParseAction(lambda tokens: PGNative(float(tokens[0])))


__all__ = ['PGNative']

class PGNative(HasComponents):
    short = 'native'
    
    def __init__(self, value):
        if isinstance(value, PGNative):
            msg = 'Could not give %r as value of PGNative' % value
            raise ValueError(msg)
        self.value = value

    @staticmethod
    def get_parsing_expr():
        return True, integer  # | floatnumber
            
    def get_components(self):
        return []
    
    def match(self, variables, other):  # @UnusedVariable
        if not(self.value == other.value):
            raise FailedMatch(self, other)
    
    def replace_vars(self, variables):  # @UnusedVariable
        return self
    
    def __repr__(self):
        return 'PGNative(%r)' % self.value
    
    def __str__(self):
        return self.value.__repr__()
    
    @staticmethod
    def get_parsing_examples():
        return """
            1
            2
        """
        

