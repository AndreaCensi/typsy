from genblocks.unittests.test_registrar import good, good_parsing_examples
from sts.parsing.parsin import parse_spec
from sts.parsing.testing import get_all_embedded_examples

good(
"""
{0,1}
{0,1,2}
{0}
({0,1})^($n)
1
BB({0,1};{0,1};2)
({0})x({0,1})

({0,1})->({0,1})


"""
)

bad = """
{0}x{0,1}
"""

def test_examples():
    for a, _ in good_parsing_examples:
        yield check_example, a

                
def test_embedded_examples():
    for a in get_all_embedded_examples():
        yield check_example, a
        
def check_example(s):
        print('check %r' % s)
#     try:
        p = parse_spec(s)
        print('parsed as %r' % p)
        s2 = str(p)
        print('rewritten as %r' % s2)
        p2 = parse_spec(s2)
        print('reparsed as %r' % p2)
        assert p == p2
#     except (TypeError, Exception) as e:
#         print('error')
#         print e
#         assert False

# 
# def test_finite_set():
#     from genblocks.finite_set import FiniteSet
#     _, expr = FiniteSet.get_parsing_expr()
#     parse_spec('{0}', expr)
