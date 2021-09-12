from .Fragment import Fragment
from utils.flags import *
from utils.CustomLogging import CustomLogging
from python_compiler.engines.utils.types import get_python_type_str, ANY

def get_for_code(fragment) -> str:
    if not (code := fragment.get(ATTRIBUTE_FOR_CODE)):
        CustomLogging.critical(f"Required Fragment type for '{ATTRIBUTE_FOR_CODE}' attribute does not exist")
    return code

def get_for_else_code(fragment) -> str:
    if not (code := fragment.get(ATTRIBUTE_FOR_ELSE_CODE)):
        CustomLogging.critical(f"Required Fragment type for '{ATTRIBUTE_FOR_ELSE_CODE}' attribute does not exist")
    return code

def get_for_iterators(fragment) -> list:
    if not (iterators := fragment.get(ATTRIBUTE_FOR_ITERATORS)):
        CustomLogging.critical(f"Required Fragment type for '{ATTRIBUTE_FOR_ITERATORS}' attribute does not exist")
    return iterators

def get_for_sequence(fragment) -> list:
    if not (sequence := fragment.get(ATTRIBUTE_FOR_SEQUENCE)):
        CustomLogging.critical(f"Required Fragment type for '{ATTRIBUTE_FOR_SEQUENCE}' attribute does not exist")
    return sequence


class For(Fragment):
    iterators:list
    sequence:str 
    code:list
    else_code:list
    def __init__(self, blueprint, *args, **kwargs) -> None:
        super().__init__( blueprint, *args, **kwargs)
        self.iterators = get_for_iterators(blueprint)
        self.sequence = get_for_sequence(blueprint)
        self.code = get_for_code(blueprint)
        self.else_code = get_for_else_code(blueprint)
    
    def iterators_compile(self) -> str:
        iterators_build = ", ".join(self.iterators)
        return iterators_build
    
    def get_lines(self) -> list:
        fragment_lines = []
        fragment_lines.append(f"for {self.iterators_compile()} in {self.sequence}:")
        fragment_lines.extend(self.code_lines_compile(self.code))
        fragment_lines.append("else:")
        fragment_lines.extend(self.code_lines_compile(self.else_code))
        fragment_lines = self.tabulate(fragment_lines)
        return fragment_lines

    def compile(self) -> str:
        fragment_build = "\n".join(self.get_lines())
        return fragment_build