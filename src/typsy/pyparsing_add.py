from pyparsing import Or, ParseException
import sys


class MyOr(Or):
    """ Make better error message """
    
    def parseImpl(self, instring, loc, doActions=True):
        maxExcLoc = -1
        maxMatchLoc = -1
        maxException = None

        exceptions = []
        
        for e in self.exprs:
            try:
                loc2 = e.tryParse(instring, loc)
            except ParseException as pe:
                e_exception = pe 
                exceptions.append((e, e_exception))
            except IndexError:
                e_exception = ParseException(instring, len(instring), e.errmsg, self)
                exceptions.append((e, e_exception))
            else:
                if loc2 > maxMatchLoc:
                    maxMatchLoc = loc2
                    maxMatchExp = e

        if maxMatchLoc < 0:
            if exceptions:
                msg = 'Could not match any of the %d alternatives:' % len(self.exprs)
                for e, e_exception in exceptions:
                    msg += '\n%20s: %20s' % (e, e_exception)
                raise ParseException(instring, loc, msg, self)
            else:
                raise ParseException(instring, loc, "no defined alternatives to match", self)

        return maxMatchExp._parse(instring, loc, doActions)


def wrap_parse_action(parse_action):
    def f(s, loc, tokens):
        print('wrap(%s):\n  %r\n -> %r' % (parse_action.__name__, s[loc:], tokens))
        try:
            res = parse_action(s, loc, tokens)
            
            print(' -> %s' % res)
            print('    %r' % res)
            return res
        except (TypeError, Exception) as e:
            print('Exception while executing %r' % parse_action)
            print(' %s' % e)
            raise
    return f
    
