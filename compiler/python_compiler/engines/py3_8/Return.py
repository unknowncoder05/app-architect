from .Fragment import Fragment
from utils.flags import *
from utils.CustomLogging import CustomLogging
from python_compiler.engines.utils.types import get_python_type_str, ANY

def get_return_attributes(fragment) -> list:
    if not (return_attributes := fragment.get(ATTRIBUTE_FUNCTION_RETURN_ARGS)):
        return_attributes = []
    return return_attributes

class Return(Fragment):
    return_attributes:list
    def __init__(self, blueprint, *args, **kwargs) -> None:
        super().__init__( blueprint, *args, **kwargs)
        self.return_attributes = get_return_attributes(blueprint)
    
    def return_compile(self) -> list:
        return_attributes_build = ", ".join(self.return_attributes)
        return_fragment_build = f"return {return_attributes_build}"
        return [return_fragment_build]
    
    def get_lines(self) -> list:
        fragment_lines = []
        fragment_lines.extend(self.return_compile())
        fragment_lines = self.tabulate(fragment_lines)
        return fragment_lines
    
    def compile(self) -> str:
        fragment_build = "\n".join(self.get_lines())
        return fragment_build