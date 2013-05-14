from typsy.parsing.testing import get_all_embedded_examples
from typsy.parsing.parsin import parse_spec


def test_embedded_examples():
    for a in get_all_embedded_examples():
        yield check_example, a
        
def check_example(s):
    print('check %r' % s)
    p = parse_spec(s)
    print('parsed as %r' % p)
    s2 = str(p)
    print('rewritten as %r' % s2)
    p2 = parse_spec(s2)
    print('reparsed as %r' % p2)
    assert p == p2
         
