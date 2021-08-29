from .Fragment import Fragment
from .FunctionArgs import FunctionArgs
from utils.flags import *
from utils.CustomLogging import CustomLogging
from python_compiler.engines.utils.types import get_python_type_str, ANY

def get_function_name(fragment) -> str:
    if not (function_name := fragment.get(ATTRIBUTE_FUNCTION_NAME)):
        CustomLogging.critical(f"Fragment type functions 'name' attribute does not exist")
    return function_name

def get_function_args(fragment) -> dict:
    if not (function_args := fragment.get(ATTRIBUTE_FUNCTION_ARGS)):
        function_args = {}
    return function_args

def get_function_kwargs(fragment) -> dict:
    if not (function_kwargs := fragment.get(ATTRIBUTE_FUNCTION_KWARGS)):
        function_kwargs = {}
    return function_kwargs

def get_function_outputs(fragment) -> dict:
    if not (function_outputs := fragment.get(ATTRIBUTE_FUNCTION_OUTPUTS)):
        function_outputs = {}
    return function_outputs

def get_function_code(fragment) -> dict:
    if not (function_code := fragment.get(ATTRIBUTE_FUNCTION_CODE)):
        function_code = {}
    return function_code

class Function(Fragment):
    name:str
    args:dict
    kwargs:dict
    outputs:dict
    def __init__(self, blueprint, *args, **kwargs) -> None:
        super().__init__( blueprint, *args, **kwargs)
        self.name = get_function_name(blueprint)
        self.args = get_function_args(blueprint)
        self.kwargs = get_function_kwargs(blueprint)
        self.outputs = get_function_outputs(blueprint)
        self.code = get_function_code(blueprint)
    def inputs_compile(self) -> str:
        inputs_build = ""
        if self.args:
            function_args = FunctionArgs(self.args, compile=self.general_compile)
            inputs_build += function_args.compile()
        
        if self.kwargs:
            function_kwargs = FunctionArgs(self.kwargs, compile=self.general_compile)
            if self.args:
                inputs_build += "," # TODO: disguisting but effective
            inputs_build += f" *, {function_kwargs.compile()}"
        return inputs_build
    def outputs_compile(self) -> str:
        outputs_build = ""
        if len(self.outputs) == 1:
            if not (arg_type_name := self.outputs[list(self.outputs)[0]].get(ATTRIBUTE_TYPE)): # TODO: Temporal Outoput test
                arg_type_name = ANY
            outputs_build += f"->{get_python_type_str(arg_type_name)}"
        return outputs_build
    def code_lines_compile(self) -> list:
        code_build_lines = []
        for line in self.code:
            code_build_lines.append(TAB*(self.level+1)+self.general_compile(line, level=self.level+1))
        return code_build_lines
    def compile(self)->str:
        fragment_lines = []
        fragment_lines.append(f"def {self.name}({self.inputs_compile()}){self.outputs_compile()}:")
        fragment_lines.extend(self.code_lines_compile())
        fragment_build = "\n".join(fragment_lines)
        
        return fragment_build