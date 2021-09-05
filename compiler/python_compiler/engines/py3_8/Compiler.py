from utils.flags import *
from .get_fragment_class import get_fragment_class


def lines_compile(blueprint:dict, *, level = 0)->str:
    build = get_fragment_class(blueprint, lines_compile, level=level)
    return build.get_lines()

def compile(blueprint:dict, *, level = 0)->str:
    build = get_fragment_class(blueprint, lines_compile, level=level)
    return build.compile()
