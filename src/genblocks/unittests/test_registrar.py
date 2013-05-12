from contracts import contract

good_parsing_examples = []
syntax_fail_examples = []

# If exact is True, we are providing a canonical form
# for the expression and we want it back.

@contract(a='str')
def good(a, exact=True):
    for s in a.split('\n'):
        s = s.strip()
        if s:
            good_parsing_examples.append((s, exact))


def syntax_fail(s):
    syntax_fail_examples.append(s)

# 
# def semantic_fail(a, b, exact=True):
#     semantic_fail_examples.append((a, b, exact))
# 
# 
# 
# def fail(a, b, exact=True):
#     contract_fail_examples.append((a, b, exact))


