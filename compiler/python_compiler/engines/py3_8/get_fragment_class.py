from .Fragment import Fragment
from .Function import Function
from utils.flags import *
from utils.CustomLogging import CustomLogging
FRAGMENT_TYPES={
    "function": Function,
    "class":Fragment,
    "variable":Fragment,
    "conditional":Fragment,
    "return":Fragment
}

def get_fragment_class(blueprint):
    if fragment_type := blueprint.get(ATTRIBUTE_FRAGMENT_TYPE):
        if fragment_class := FRAGMENT_TYPES[fragment_type]:
            return fragment_class(blueprint)
        else:
            CustomLogging.error(f"Fragment type {fragment_type} does not exists")
    else:
        CustomLogging.error(f"Flag {ATTRIBUTE_FRAGMENT_TYPE} not defined in blueprint")