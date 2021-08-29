from .Fragment import Fragment
from utils.flags import *
from utils.CustomLogging import CustomLogging
from python_compiler.engines.utils.types import get_python_type_str, ANY

def get_conditional_condition(fragment) -> str:
    if not (condition := fragment.get(ATTRIBUTE_CONDITIONAL_CONDITION)):
        CustomLogging.critical(f"Fragment type conditional '{ATTRIBUTE_CONDITIONAL_CONDITION}' attribute does not exist")
    return condition

def get_conditional_code(fragment) -> list:
    if not (code := fragment.get(ATTRIBUTE_CONDITIONAL_CODE)):
        CustomLogging.critical(f"Fragment type conditional '{ATTRIBUTE_CONDITIONAL_CODE}' attribute does not exist")
    return code
class Conditional(Fragment):
    condition:str
    code:list
    def __init__(self, blueprint, *args, **kwargs) -> None:
        super().__init__( blueprint, *args, **kwargs)
        self.condition = get_conditional_condition(blueprint)
        self.code = get_conditional_code(blueprint)
    def code_lines_compile(self) -> list:
        code_build_lines = []
        for line in self.code:
            code_build_lines.append(TAB*(self.level+1)+self.general_compile(line))
        return code_build_lines
    def compile(self)->str:
        fragment_lines = []
        fragment_lines.append(f"if {self.condition}:")
        fragment_lines.extend(self.code_lines_compile())
        fragment_build = "\n".join(fragment_lines)
        
        return fragment_build