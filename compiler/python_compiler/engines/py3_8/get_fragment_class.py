from utils.flags import *
from utils.CustomLogging import CustomLogging

from .Fragment import Fragment
from .Function import Function
from .Class import Class
from .Variable import Variable
from .Conditional import Conditional
from .FunctionCall import FunctionCall
from .Return import Return
from .For import For


FRAGMENT_TYPES={
    "class": Class,
    "function": Function,
    "function_call":FunctionCall,
    "variable":Variable,
    "conditional":Conditional,
    "return":Return,
    "for":For
}

def get_fragment_class(blueprint, compile, *, level=0):
    if fragment_type := blueprint.get(ATTRIBUTE_FRAGMENT_TYPE):
        if fragment_class := FRAGMENT_TYPES[fragment_type]:
            return fragment_class(blueprint, compile=compile, level=level)
        else:
            CustomLogging.error(f"Fragment type {fragment_type} does not exist")
    else:
        CustomLogging.error(f"Flag {ATTRIBUTE_FRAGMENT_TYPE} not defined in blueprint")