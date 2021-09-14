from utils.flags import *
from python_compiler.utils.flags import *
from .get_fragment_class import get_fragment_class


def lines_compile(blueprint:dict, *, level = 0)->str:
    build = get_fragment_class(blueprint, lines_compile, level=level)
    return build.get_lines()

def compile(blueprint:dict, *, level = 0):
    builder = get_fragment_class(blueprint, lines_compile, level=level)
    return builder.get_imports(), builder.compile()
