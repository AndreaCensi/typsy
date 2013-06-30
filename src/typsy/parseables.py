# -*- coding: utf8 -*-
from typsy.has_comps import HasComponents, simple_sts_type, sts_type
from pyparsing import Literal, Suppress, OneOrMore
from contracts import contract
from typsy.pyparsing_add import MyOr, wrap_parse_action

    
class Parseable(HasComponents):
    
    PRECEDENCE_VARIABLE = 0
    PRECEDENCE_SIMPLE_STRING = 0
    PRECEDENCE_COMPOSITE = 0.4  # SP(A;B)
    PRECEDENCE_FINITE_SET = 0
    
    @classmethod
    def get_parsing_expr(klass):
        msg = 'Need to implement get_parsing_expr() for %s' % klass
        raise NotImplementedError(msg)

    @classmethod
    def get_parsing_examples(klass):
        msg = 'Need to implement get_parsing_examples() for %s' % klass
        raise NotImplementedError(msg)

    @classmethod
    def get_precedence(klass):
        msg = 'Need to implement get_precedence() for %s' % klass
        raise NotImplementedError(msg)

    def format_sub(self, x):
        """ returns either (x) or x whether one is needed """
        s = '%s' % x
        if not isinstance(x, Parseable):
            msg = 'I expect a parseable object, got %r' % x
            raise ValueError(msg)
        p1 = type(x).get_precedence()
        p2 = type(self).get_precedence()
        if p1 >= p2:
            s = '(%s)' % s
        return s
    
    
class ParseableWithOperators(Parseable):
    precedence = {
        '->': 2,
        '⟶': 2,
        'x': 0.3,
        '×': 0.3,
        "∩": 0.3,
        "^": 0.3
    }
    
    TWO_OR_MORE = '2+'
    
    @classmethod
    def get_arity(klass):
        """ either 2 or TWO_OR_MORE """ 
        msg = 'Need to implement get_arity() for %s' % klass
        raise NotImplementedError(msg)

    @classmethod
    @contract(returns='list(tuple(str,*))')
    def get_subs(klass):
        """ 
            Returns subs and types of the components.
            These will be passed to the constructor.
        """ 
        pass

    @classmethod
    @contract(returns='list(str)')
    def get_glyphs(klass):
        """
            First glyph must be in ParseableWithOperators.precedence
        """ 
        msg = 'Need to implement get_glyphs() for %s' % klass
        raise NotImplementedError(msg)
    
    @classmethod
    def get_glyph_for_output(klass):
        glyphs = klass.get_glyphs()
        # TODO: implement unicode switch
        return glyphs[0]
        
    @classmethod
    def get_precedence(klass):
        glyph1 = klass.get_glyphs()[0]
        if not glyph1 in ParseableWithOperators.precedence:
            msg = 'Could not find glyph %r for cls %r in precedence' % (glyph1, klass)
            raise ValueError(msg)
        return ParseableWithOperators.precedence[glyph1]

    @classmethod
    def get_parsing_expr(klass):
        if klass.get_arity() == 2:
            raise Exception(klass)
        S = Suppress
        L = Literal
        inside = simple_sts_type | (S('(') - sts_type - S(')'))        
        
        glyphs = klass.get_glyphs()
        glyph = S(MyOr(map(L, glyphs)))
        
        arity = klass.get_arity()
        if arity == 2:
            expr = (inside + glyph + inside)
        elif arity == ParseableWithOperators.TWO_OR_MORE:
            expr = (inside + OneOrMore(glyph + inside))
        else:
            raise NotImplementedError(arity)
        
        def my_parse_action(s, loc, tokens):  # @UnusedVariable
            if arity == 2:
                a = tokens[0]
                b = tokens[1]
                return klass(a, b)
            elif arity == ParseableWithOperators.TWO_OR_MORE:
                return klass(*tuple(tokens))
            else:
                raise NotImplementedError()
                
        expr.addParseAction(wrap_parse_action(my_parse_action))
        expr.setName(klass.__name__)
        return False, expr
    
    @classmethod
    def op_system_parse_action(klass, s, loc, tokens):  # @UnusedVariable
        # print('here %s %s %s' % (s, loc, tokens))
        vals = list(tokens[0])    
        arity = klass.get_arity()
        if arity == 2:        
            # we get [Variable('A'), '->', Variable('B'), '->', Variable('C')]

            exprs = [vals.pop(0)]
            while vals:
                glyph = vals.pop(0)
                assert isinstance(glyph, str)
                expr = vals.pop(0)
                assert isinstance(expr, HasComponents)
                exprs.append(expr)
                
            # exprs = Variable('A'), Variable('B'), Variable('C')
            def f(exs):
                if len(exs) == 2:
                    return klass(exs[0], exs[1])
                else:
                    return klass(exs[0], f(exs[1:]))

            return f(exprs)

        elif arity == ParseableWithOperators.TWO_OR_MORE:
#             res = klass(*tuple(tokens))
#         else:
            raise NotImplementedError()

    
    def __str__(self):
        ss = []
        cv = list(self.get_components_and_values())
        arity = type(self).get_arity()
        if arity == 2:
            for _, v in cv:
                ss.append(self.format_sub(v))
        elif arity == ParseableWithOperators.TWO_OR_MORE:
            assert len(cv) == 1, 'We expect only one component pointing to a tuple'
            values = cv[0][1]
            for v in values:
                ss.append(self.format_sub(v))
        else:
            raise NotImplementedError()
        glyph = type(self).get_glyph_for_output()
        inter = " %s " % glyph
        s = inter.join(ss)
        return s
    

class ParseableAsString(Parseable):
    
    @classmethod
    def get_precedence(klass):  # @UnusedVariable
        return Parseable.PRECEDENCE_SIMPLE_STRING
    
    @classmethod
    def get_identifier(klass):
        msg = 'Need to implement get_glyphs() for %s' % klass
        raise NotImplementedError(msg)
    
    def __str__(self):
        return type(self).get_identifier()
    
    @classmethod
    def get_parsing_expr(klass):
        identifier = klass.get_identifier()
        
        S = Suppress
        L = Literal
        expr = S(L(identifier))
        expr.setName(identifier)
        
        def parse_action(s, loc, tokens):  # @UnusedVariable
            return klass()
        
        expr.setParseAction(parse_action)
        return True, expr
   
class ParseableWithExpression(Parseable):
    """
        This is an expression of the kind
        
            SP(A;B;...)
            
        where 
            arity
    """
    
    @classmethod
    def get_arity(cls):
        """ Number of elements inside """
        return len(cls.get_components())
    
    @classmethod
    def get_identifier(cls):
        """ "SP" """
        raise NotImplementedError(cls)
    
    @classmethod
    def get_glyph(cls):
        """ Inner glyph """
        return ';'

    @classmethod
    def get_precedence(cls):
        return Parseable.PRECEDENCE_COMPOSITE
     
    @classmethod
    def get_parsing_expr(klass):
        L = Literal
        S = Suppress
        start = S(L(klass.get_identifier()))
        glyph = S(L(klass.get_glyph())) 
        n = klass.get_arity()
        assert n >= 1
        inside = sts_type 
        for _ in range(n - 1):
            inside = inside + glyph + sts_type
    
        expr = start + S(L('(')) + inside + S(L(')'))
        expr.setName(klass.get_identifier())
        
        def parse_action(s, loc, tokens):  # @UnusedVariable
            tokens = list(tokens)
            return klass(*tokens)
        
        expr.setParseAction(parse_action)
        return True, expr
    
    def __str__(self):
        cls = type(self)
        ss = []
        cv = list(self.get_components_and_values())
        for _, v in cv:
            
            try:
                vs = self.format_sub(v)
            except:
                vs = '!!!'

            ss.append(vs)

        glyph = cls.get_glyph()
        inter = "%s " % glyph
        identifier = cls.get_identifier()
        s = identifier + '(' + inter.join(ss) + ')'
        return s
