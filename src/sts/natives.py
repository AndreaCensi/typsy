from sts.has_comps import HasComponents
from sts.exceptions import FailedMatch
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



class PGNative(HasComponents):
    short = 'native'
    
    @staticmethod
    def get_parsing_expr():
        return True, integer  # | floatnumber
        
    def __init__(self, value):
        if isinstance(value, PGNative):
            msg = 'Could not give %r as value of PGNative' % value
            raise ValueError(msg)
        self.value = value
        
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
        
class PGList(list, HasComponents):
    short = 'list'
    
    def match(self, variables, other):
        for s1, s2 in zip(self, other):
            HasComponents.debug_level += 1
            s1.match(variables, s2)
            HasComponents.debug_level -= 1
    
    def replace_vars(self, variables):
        l = [c.replace_vars(variables) for c in self]
        return PGList(l)

    @staticmethod
    def get_parsing_expr():
        return None
    
def as_gb(value):
    if isinstance(value, HasComponents):
        return value  
    if isinstance(value, list):
        return PGList(map(as_gb, value))
    else:
        return PGNative(value)

