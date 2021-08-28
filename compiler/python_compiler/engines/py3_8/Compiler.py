from utils.flags import *
from .get_fragment_class import get_fragment_class


def compile(blueprint:dict)->str:
    build = get_fragment_class(blueprint)
    return build.compile()
