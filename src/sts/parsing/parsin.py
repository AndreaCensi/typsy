from contracts import contract
import yaml
from pprint import pformat
from sts.has_comps import HasComponents, get_sts_type
from sts.natives import PGNative, PGList
from sts.variable import Variable
from pyparsing import ParseException, ParseFatalException
from contracts.interface import Where, ContractSyntaxError

@contract(string='str')
def parse_spec(string, expr=None):
    if expr is None:
        expr = get_sts_type()
    try:
        c = expr.parseString(string, parseAll=True)[0]
        assert isinstance(c, HasComponents), 'Want HasComponents, not %r' % c
        return c
    except (ParseException, ParseFatalException) as e:
        where = Where(string, line=e.lineno, column=e.col)
        msg = '%s' % e
        raise ContractSyntaxError(msg, where=where)


def parse_yaml_spec(s):
    p = GBParser()
    r = p.parse_struct(s)
    return r


class GBParser():
    def __init__(self):
        self.names = set()
        
    def instance(self, klass, **kwargs):
        try: 
            return klass(**kwargs)
        except TypeError as e:
            msg = 'Cannot call %r %r' % (klass, 'kwargs')
            msg += '\n%s' % e
            raise Exception(msg)
        
    def parse_pair(self, k, v):
        klasses = HasComponents.klasses 
        if k in klasses:
            if not isinstance(v, dict):
                msg = 'Expected %r dict' % v
                raise ValueError(msg)
            klass = klasses[k]
            vals = dict([(m, self.parse_value(x)) for m, x in v.items()]) 
            return self.instance(klass, **vals)

        msg = 'could not interpret %r' % k
        raise Exception(msg)
    
    @contract(s=str)
    def parse_struct(self, s):
        x = yaml.load(s)
        print pformat(x)
        return self.parse_root(x)
    
    def parse_value(self, x):
        if isinstance(x, (int, float)):
            return PGNative(x)
        if isinstance(x, list):
            m = map(self.parse_value, x)
            l = PGList()
            l.extend(m)
            return l
        return self.parse_root(x)
        
    @contract(x='str|dict[1]')
    def parse_root(self, x):
        if isinstance(x, str):
            if x[0] == '$':
                return Variable(x[1:])
            else:
                if x in HasComponents.names:
                    return HasComponents.names[x]
                else:
                    return x
                    # msg = 'Could not interpret %r' % x
                    # raise Exception(msg)
    
        assert len(x) == 1
        k = list(x.keys())[0]
        v = list(x.values())[0]
        return self.parse_pair(k, v)

