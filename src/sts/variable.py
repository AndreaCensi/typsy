from pyparsing import (alphanums, alphas, Word, oneOf, Combine, Literal, Suppress,
    Optional)
from sts import HasComponents
from sts.exceptions import FailedMatch


class Variable(HasComponents):
    short = 'variable'
    
    def __init__(self, name):
        self.name = name
        
    def get_components(self):
        return []
    
    def match(self, variables, other):
        self.debug('match (vars: %s)' % variables)
        if self.name in variables:
            v = variables[self.name]
            self.debug('variable already found = %s' % v)
            if v == self:
                self.debug('variable is me!')
                return  # XXX 
                # raise ValueError()
            if isinstance(v, HasComponents):
                HasComponents.debug_level += 1
                v.match(variables, other)
                HasComponents.debug_level -= 1
            else:
                if v != other:
                    raise FailedMatch(v, other) 
        else:
            self.debug('Setting variable to %s' % other)
            variables[self.name] = other

    def replace_vars(self, variables):
        self.debug('replace_vars')
        return variables[self.name]
 
    def __str__(self):
        return '$' + self.name
    
    def __repr__(self):
        return 'Variable(%r)' % self.name

    @staticmethod
    def get_parsing_expr():
        S = Suppress
        O = Optional
        identifier_expression = Combine(oneOf(list(alphas)) + O(Word('_' + alphanums)))
        expr = S(Literal('$')) - identifier_expression
        expr.setName('variable')
        
        def my_parse_action(s, loc, tokens):  # @UnusedVariable
            name = tokens[0]
            return Variable(name)
                
        expr.addParseAction(my_parse_action)
        return True, expr
        
