from contracts import contract
from pyparsing import ParseException, ParseFatalException
from contracts.interface import Where, ContractSyntaxError
from typsy.has_comps import get_sts_type, HasComponents


@contract(string='str')
def parse_spec(string, expr=None):
    if expr is None:
        expr = get_sts_type()
    try:
        c = expr.parseString(string, parseAll=True)[0]
        assert isinstance(c, HasComponents), 'Want HasComponents, not %r' % c
        return c
    except (ParseException, ParseFatalException) as e:
#         raise  # XXX
        where = Where(string, line=e.lineno, column=e.col)
        msg = '%s' % e
        msg += '\nelement: %r' % e.parserElement 
        raise ContractSyntaxError(msg, where=where)
        
