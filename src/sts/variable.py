from pyparsing import (alphanums, alphas, Word, oneOf, Combine, Literal, Suppress,
    Optional)
from sts import HasComponents
from sts.exceptions import FailedMatch
from sts.intersections import Intersection


class Variable(HasComponents):
    short = 'variable'
    
    def __init__(self, name):
        self.name = name
        
    def __eq__(self, other):
        if not isinstance(other, Variable):
            return False
        return self.name == other.name
        
    def get_components(self):
        return []
    
    def match(self, variables, other):
        self.debug('match variable %r with %r (vars: %s)' 
                   % (self, other, variables))
        if self.name in variables:
            v = variables[self.name]
            
            variables[self.name] = Intersection([v, other])
#             
#             self.debug('variable already found = %s' % v)
#             if v == self: 
#                 raise ValueError()
#             if isinstance(v, HasComponents):
#                 HasComponents.debug_level += 1
#                 v.match(variables, other)
#                 HasComponents.debug_level -= 1
#             else:
#                 if v != other:
#                     raise FailedMatch(v, other) 
        else:
            self.debug('Setting constraint %s satisfies  %s' % (self.name, other))
            variables[self.name] = other

    def replace_vars(self, variables):
        # self.debug('replace_vars')
        if self.name in variables:
            return variables[self.name]
        else:
            return self
 
    def get_variables(self):
        return {self.name: self}
     
    def __str__(self):
        if len(self.name) == 1:
            return self.name
        else:
            return '$' + self.name
    
    def __repr__(self):
        return 'Variable(%r)' % self.name

    @staticmethod
    def get_parsing_expr():
        S = Suppress
        O = Optional
        identifier_expression = Combine(oneOf(list(alphas)) + O(Word('_' + alphanums)))
        expr = S(Literal('$')) - identifier_expression
        expr = expr ^ oneOf(list(alphas))
        expr.setName('variable')
        
        def my_parse_action(s, loc, tokens):  # @UnusedVariable
            name = tokens[0]
            return Variable(name)
                
        expr.addParseAction(my_parse_action)
        return True, expr
        
