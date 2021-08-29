from utils.flags import *
from .get_fragment_class import get_fragment_class


def compile(blueprint:dict, *, level = 0)->str:
    build = get_fragment_class(blueprint, compile, level=level)
    return build.compile()
