from contracts import new_contract
contract_inherit = lambda x: x


 
@new_contract
def space(x):
    pass

@new_contract
def in_input(x):
    pass

@new_contract
def in_output(x):
    pass

@new_contract
def in_space(x):
    pass


from .bb import *
from .orbit_space import *
from .product import *
from .group_action import *
from .common import *
from .stochastic_process import *
from .configurations import *
