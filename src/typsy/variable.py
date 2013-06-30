from pyparsing import (alphanums, alphas, Word, oneOf, Combine, Literal, Suppress,
    Optional)

from typsy.intersection import Intersection
from typsy.parseables import Parseable
from typsy.pyparsing_add import wrap_parse_action
from contracts import contract


class Variable(Parseable):
    
    @classmethod
    def get_precedence(cls):
        return Parseable.PRECEDENCE_VARIABLE
    
    def __init__(self, name):
        self.name = name
        
    def __eq__(self, other):
        if not isinstance(other, Variable):
            return False
        return self.name == other.name
        
    @classmethod
    def create_from_kwargs(cls, kwargs):
        return Variable[kwargs['name']]
    
    @classmethod
    def get_components(cls):
        return []
    
    def match(self, variables, other):
#        self.debug('match variable %r with %r (vars: %s)' 
#                   % (self, other, variables))
        if self.name in variables:
            v = variables[self.name]            
            variables[self.name] = Intersection(v, other)
        else:
            # self.debug('Setting constraint %s satisfies  %s' % (self.name, other))
            variables[self.name] = other

    def replace_vars(self, variables):
        if self.name in variables:
            return variables[self.name]
        else:
            return self
 
    def reduce(self):
        return self
    
    def get_variables(self):
        return set([self.name])
     
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
                
        expr.addParseAction(wrap_parse_action(my_parse_action))
        return True, expr
        
    @staticmethod
    def get_parsing_examples():
        return """
        A
        $A
        $b
        """
        
    def replace_used_variables(self, already_taken, substitutions):
        if self.name in substitutions:
            # We have already decided how to transform this one
            return Variable(substitutions[self.name])
        
        if self.name in already_taken:
            # we need to substitute this one
            dont_use = set([self.name]) | set(already_taken) | set(substitutions.values())
            new_name = get_new_name(dont_use=dont_use)
            substitutions[self.name] = new_name
            return Variable(new_name)
        
        substitutions[self.name] = self.name
        return Variable(self.name)
        
@contract(returns='str', dont_use='set(str)')    
def get_new_name(dont_use):
    """ Returns a new name, not included in "dont_use". """
    variables = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                  'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'Z']
    for v in variables:
        if not v in dont_use:
            return v
        
    # TODO: need more names
    raise ValueError('xxx')
    
    
    

