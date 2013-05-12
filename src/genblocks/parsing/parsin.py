from contracts import contract
from genblocks.interfaces import Mapping
from genblocks.product import Product, ProductSpace
import yaml
from pprint import pformat
from genblocks.bb import BlackBox
from genblocks.orbit_space import OrbitSpace
from genblocks.common import bit, Interval
from genblocks.group_action import GProduct, Automorphism
from genblocks.stochastic_process import StochasticProcess
from genblocks.variable import Variable

names = {
    'map': Mapping,
    'prod': Product,
    'gprod': GProduct,
    'bb': BlackBox,
    'os': OrbitSpace,
    'bit': bit,
    'interval': Interval,
    'aut': Automorphism,
    'product': ProductSpace,
    'sp': StochasticProcess
}

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
            msg = 'Cannot call %s %s' % (klass, kwargs)
            msg += '\n%s' % e
            raise Exception(msg)
        
    def parse_pair(self, k, v):
        if k in names:
            if not isinstance(v, dict):
                msg = 'Expected %r dict' % v
                raise ValueError(msg)
            klass = names[k]
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
            return x
        if isinstance(x, list):
            return map(self.parse_value, x)
        return self.parse_root(x)
        
    @contract(x='str|dict[1]')
    def parse_root(self, x):
        if isinstance(x, str):
            if x[0] == '$':
                return Variable(x[1:])
            else:
                if x in names:
                    return names[x]
                else:
                    msg = 'Could not interpret %r' % x
                    raise Exception(msg)
        
        assert len(x) == 1
        k = list(x.keys())[0]
        v = list(x.values())[0]
        return self.parse_pair(k, v)

