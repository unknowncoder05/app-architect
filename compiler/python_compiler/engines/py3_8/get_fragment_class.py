from utils.flags import *
from utils.CustomLogging import CustomLogging

from .Fragment import Fragment
from .Function import Function
from .Variable import Variable
from .Conditional import Conditional
from .FunctionCall import FunctionCall
from .Return import Return


FRAGMENT_TYPES={
    "function": Function,
    "function_call":FunctionCall,
    "class":Fragment,
    "variable":Variable,
    "conditional":Conditional,
    "return":Return
}

def get_fragment_class(blueprint, compile, *, level=0):
    if fragment_type := blueprint.get(ATTRIBUTE_FRAGMENT_TYPE):
        if fragment_class := FRAGMENT_TYPES[fragment_type]:
            return fragment_class(blueprint, compile=compile, level=level)
        else:
            CustomLogging.error(f"Fragment type {fragment_type} does not exist")
    else:
        CustomLogging.error(f"Flag {ATTRIBUTE_FRAGMENT_TYPE} not defined in blueprint")