from .Fragment import Fragment
from utils.flags import *
from utils.CustomLogging import CustomLogging
from python_compiler.engines.utils.types import get_python_type_str, ANY

def get_function_name(fragment) -> str:
    if not (function_name := fragment.get(ATTRIBUTE_FUNCTION_CALL_NAME)):
        CustomLogging.critical(f"Required Fragment type function_call '{ATTRIBUTE_FUNCTION_CALL_NAME}' attribute does not exist")
    return function_name

def get_function_args(fragment) -> dict:
    if not (function_args := fragment.get(ATTRIBUTE_FUNCTION_ARGS)):
        function_args = {}
    return function_args

def get_function_kwargs(fragment) -> dict:
    if not (function_kwargs := fragment.get(ATTRIBUTE_FUNCTION_KWARGS)):
        function_kwargs = {}
    return function_kwargs

class FunctionCall(Fragment):
    name:str
    args:dict
    kwargs:dict
    def __init__(self, blueprint, *args, **kwargs) -> None:
        super().__init__( blueprint, *args, **kwargs)
        self.name = get_function_name(blueprint)
        self.args = get_function_args(blueprint)
        self.kwargs = get_function_kwargs(blueprint)
    def inputs_compile(self) -> str:
        inputs = []
        if self.args:
            inputs = self.args
        
        if self.kwargs:
            inputs.extend([ f"{x}={self.kwargs[x]}" for x in self.kwargs])

        inputs_build = ", ".join(inputs)
        return inputs_build
    
    def get_lines(self) -> list:
        fragment_lines = []
        fragment_lines.append(f"{self.name}({self.inputs_compile()})")
        fragment_lines = self.tabulate(fragment_lines)
        return fragment_lines

    def compile(self) -> str:
        fragment_build = "\n".join(self.get_lines())
        return fragment_build